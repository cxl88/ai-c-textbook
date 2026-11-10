#include <stdio.h>

int main(void)
{
    int a;

    a = 10; a += 3; printf("%d\n", a);
    a = 10; a -= 3; printf("%d\n", a);
    a = 10; a *= 3; printf("%d\n", a);
    a = 10; a /= 3; printf("%d\n", a);
    a = 10; a %= 3; printf("%d\n", a);
    a = 2; a *= 4 + 1; printf("%d\n", a);
    printf("[%5.1f|%-4d]\n", 3.14159, 25);
    printf("A\tB\n");
    printf("98%%\n");
    printf("%c\n", 66);
    printf("%s\n", "OK");
    printf("%.1f %.1f %.2f\n", -12.8, 0.25, 2.675);
    a = -12.8;
    printf("%d\n", a);
    return 0;
}
