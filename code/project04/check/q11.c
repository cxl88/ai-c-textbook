#include <stdio.h>

int main(void)
{
    int a = 10, b = 3;
    float x = 7;

    a = a / b;
    x = x / 2;
    printf("%d|%5.2f|%-4d|\n", a, x, b);
    putchar('A' + a);
    putchar('\n');
    return 0;
}
