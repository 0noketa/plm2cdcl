#include <stdio.h>
#include <stdlib.h>

void put_char(unsigned c) { putchar(c); }
void put_real(float f) { printf("%0.8f", f); }
void put_real2(float (**f)[2]) { printf("%p, %f,%f", f, 0.0+(**f)[0], 0.0+(**f)[1]); }
void put_dword(unsigned i) { printf("%d", i); }
void put_word(unsigned short i) { printf("%d", i); }
void put_ln() { putchar('\n'); }
void sample_point(float (**q)[2]) {
    static float a[2] = { 12., 34. };
    float *p = &a;
    put_real2(&p);
    *q = &a;
}
