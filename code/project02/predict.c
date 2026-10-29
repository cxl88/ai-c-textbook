#include <stdio.h>

int main(void)
{
    int a = 17, b = 5, c;
    double x;

    c = a / b;
    printf("%d\n", c);
    c = a % b;
    printf("%d\n", c);
    x = a / b;
    printf("%.1f\n", x);
    x = (double)a / b;
    printf("%.1f\n", x);
    a += b * 2;
    printf("%d\n", a);
    c = a++;
    printf("%d %d\n", c, a);
    return 0;
}
