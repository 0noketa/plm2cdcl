@rem // compile_mod mod_name

@setlocal

@if exist "mod_%~1.plm"  @plm2c "mod_%~1.plm"
@if exist "dcl_%~1.plm"  @py plm2cdecl.py < "dcl_%~1.plm" > "dcl_%~1.c"

:eof

@endlocal
