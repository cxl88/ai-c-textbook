#include <stdio.h>

int main(void)
{
    int a, b, x, n;

    a = 3;
    b = 4;
    a = b;
    b = a;
    printf("a = %d, b = %d\n", a, b);
    x = 10;
    x += 5;
    x -= 3;
    x *= 2;
    printf("x = %d\n", x);
    n = 7.9;
    printf("n = %d\n", n);
    return 0;
}
