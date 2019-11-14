
# PLM to C procedure declaration translator

import re

option_verbose = False
option_stdint = False
option_double = False

ptn_var="""
([a-z_][a-z0-9_]*)(?:|\s+based\s+([a-z_][a-z0-9_]*))
"""

ptn_array="""
\(([1-9][0-9]*|0)\)(.*)
""".strip()

# $1: label, $2: var, $3: from-to expression
ptn_do="""
(?:|([a-z_][a-z0-9_\$]*)\s*\:)\s*do(?:|\s+([a-z_][a-z0-9_]*)\s*\=([0-9a-z_\(\)\+\-\*\/\<\>\=]+))\s*;
""".strip()

ptn_end="""
end(?:|\s*([a-z_][a-z0-9_\$]*))\s*;
""".strip()

ptn_proc="""
([a-z_][a-z0-9_\$]*)\s*\:\s*procedure\s*(?:|\(\s*(|[a-z_][a-z0-9_]*(?:\s*\,\s*[a-z_][a-z0-9_]*)*)\))\s*(|[a-z_][a-z0-9_]*(?:\s+[a-z_][a-z0-9_]*)*\s*)\;
""".strip()

ptn_decl = """
declare\s(?:([a-z_][a-z0-9_]*(?:\s+based\s+[a-z_][a-z0-9_]*|))|\(((?:[a-z_][a-z0-9_]*(?:\s+based\s+[a-z_][a-z0-9_]*|)(?:\s*\,\s*[a-z_][a-z0-9_]*(?:\s+based\s+[a-z_][a-z0-9_]*|))*))\))\s*([a-z0-9_\(\)\,\s\.@\']+)\;
""".strip()

def translate_type(t):
    """typed pointers are for not public procedures only.
    currently cant be used for array declarations.
    """
    ptr = ""

    while t != "":
        r = re.match(ptn_array, t)

        if r:
            ptr += " *" 

            t = r[2].strip()

            continue

        if t == "pointer":
            t = "void *"
        elif t == "integer":
            t = "int"
        elif t == "qword":
            t = ("uint64_t" if option_stdint
                else "unsigned long long")
        elif t == "dword":
            t = ("uint32_t" if option_stdint
                else "unsigned int")
        elif t == "word":
            t = ("uint16_t" if option_stdint
                else "unsigned short")
        elif t == "byte":
            t = ("uint8_t" if option_stdint
                else "unsigned char")
        elif t == "real":
            t = ("double" if option_double
                else "float")

        break

    return t + ptr

def translate_proc_attr(attr):
    attr = attr.split()
    r = ""
    c = "static"

    for i in attr:
        if i == "public":
            c = ""
        elif i == "external":
            c = "extern"
        elif i == "reentrant":
            pass
        elif i == "interrupt":
            pass
        else:
            r = translate_type(i)

    return c + " " + r

def get_var_info(v):
    """returns (name, base or empty)

    v: element of group in pl/m declare
    """
    v = v.strip().split(" ", 2)
    v = list(map(lambda x: x.strip(), v))

    name = v[0] if len(v) else ""
    base = v[2] if len(v) == 3 and v[1] == "based" else ""

    return (name, base)

def make_cptr_decl(name, base=""):
    """makes [*p] part of C pointer decl.
    """
    if base != "":
        p = "*"
        init = " = " + base
    else:
        p = ""
        init = ""

    return p + name + init

def make_cvar_decl(name, t, base=""):
    return translate_type(t) + " " + make_cptr_decl(name, base)

def make_cvars_decl(vs, t):
    r = translate_type(t)
    
    for v in vs:
        name, base = get_var_info(v)

        r += " " + make_cptr_decl(name, base) + ","

    return r[:-1]

def update_translated_params(params, vs, t):
    """returns copy of params partly updated as C-style-typed

    params: names

    vs: elements in declare

    t: pl/m type in declare
    """
    for v in vs:
        name, base = get_var_info(v)

        if base != "":
            continue

        if name in params:
            params = list(map(lambda x:
                    make_cvar_decl(x, t, base)
                        if x == name
                    else x,
                    params))

    return params

def separate_params_and_locals(params, vs):
    """returns (name-only params in vs, rest of vs)

    params: names of params as dictionary keys

    vs: array of [i] or [j based p] part of pl/m decls
    """
    ps = []
    ls = []

    for v in vs:
        name, base = get_var_info(v)

        if name in params:
            ps += [name]
        else:
            ls += [v]
    
    return (ps, ls)

if __name__ == "__main__":
    import sys

    option_verbose = False
    option_stdint = False
    option_double = False

    for arg in sys.argv:
        if arg == '-v':
            option_verbose = True
        if arg == '-stdint':
            option_stdint = True
        if arg == '-double':
            option_double = True

    # force to be a str
    s = (lambda x: str(x).strip() if x else "")

    re_do = re.compile(ptn_do)
    re_end = re.compile(ptn_end)
    re_proc = re.compile(ptn_proc)
    re_decl = re.compile(ptn_decl)

    src = sys.stdin.read().split("\n")
    src = list(filter(lambda x: not x.strip().startswith("$"), src))
    src = " ".join(src).split(";")
    src = list(map(lambda x: x.strip() + ";", src))
    src = list(filter(lambda x: x != ";", src))

    proc = {"name": "", "attr": "", "params": []}

    dpt = 0

    for i in src:
        if option_verbose:
            print("/*-  " + i + "  */")

        r = re_proc.match(i)
        
        if r:
            if dpt == 0:
                proc["attr"] = translate_proc_attr(s(r[3]))
                proc["name"] = s(r[1])
                proc["params"] = list(map(lambda x: s(x), s(r[2]).split(",")))

                if option_verbose:
                    print("/*/*proc " + proc["name"] + "*/")
            dpt += 1

            continue

        r = re_end.match(i)

        if r :
            if dpt:
                dpt -= 1

            if dpt > 0:
                continue

            if s(r[1]) == proc["name"]:
                print(proc["attr"] + " " + proc["name"] + "(" + ",".join(proc["params"]) + ");")

            if option_verbose:
                print("/* /*endproc " + proc["name"] + "*/")
            proc["name"] = ""

            continue

        r = re_decl.match(i)

        if r:
            vs = [s(r[1])] + list(map(lambda x: s(x), s(r[2]).split(",")))
            vs = list(filter(lambda x: x != "", vs))
            t = s(r[3])

            params, locals = separate_params_and_locals(proc["params"], vs)

            if dpt == 1:
                proc["params"] = update_translated_params(proc["params"], params, t)
            
            if option_verbose and len(locals):
                print("/*+ " + make_cvars_decl(locals, t) + ";  */")

