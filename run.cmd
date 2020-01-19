
@setlocal

@if "%~1"=="" goto :eof
@if not exist "%~1" goto :eof

@tcc -g -b "-DDWORD=unsigned int" "-DWORD=unsigned short" "-DBYTE=unsigned char"  %2 %3 %4 %5 %6 %7 %8 -run "%~d1%~p1%~n1.c"


:eof

@endlocal
