
@setlocal

@if "%~1"=="" goto :eof
@if not exist "%~1" goto :eof

@plm2c "%~1"
@cl /Od /DDWORD="unsigned int" /DWORD="unsigned short" /DBYTE="unsigned char" /GS /Ge /guard:cf /MDd "%~d1%~p1%~n1.c" %2 %3 %4 %5 %6 %7 %8


:eof

@endlocal
