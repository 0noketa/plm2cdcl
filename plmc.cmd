
@setlocal

@if "%~1"=="" goto :eof

@plm2c "%~1"
@cl /O0 /DDWORD="unsigned int" /DWORD="unsigned short" /DBYTE="unsigned char" /GS /Ge /MDd "%~d1%~p1%~n1.c" %2 %3 %4 %5 %6 %7 %8


:eof

@endlocal
