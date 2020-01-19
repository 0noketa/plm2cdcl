#include <stdio.h>
#include <stdlib.h>

void put_char(unsigned c) { putchar(c); }
void put_integer(short i) { printf("%hd", i); }
void put_real(float f) { printf("%0.8f", f); }
void put_dword(unsigned i) { printf("%u", i); }
void put_word(unsigned short i) { printf("%hu", i); }
void put_ln(void) { putchar('\n'); }
unsigned get_char(void) { return getchar(); }
short get_integer(void) { short r = 0; scanf("%hd", &r); return r; }
float get_real(void) { float r = 0; scanf("%f", &r); return r; }
unsigned get_dword(void) { unsigned r = 0; scanf("%u", &r); return r; }
unsigned short get_word(void) { unsigned short r = 0; scanf("%hu", &r); return r; }
