/* 程序名：logic.c
   功能：用程序验证逻辑运算的真值表 */
#include <stdio.h>

int main(void)
{
    int a, b;

    printf(" a  b   !a  a&&b  a||b\n");
    a = 0;
    b = 0;
    printf("%2d %2d %4d %5d %5d\n", a, b, !a, a && b, a || b);
    a = 0;
    b = 1;
    printf("%2d %2d %4d %5d %5d\n", a, b, !a, a && b, a || b);
    a = 1;
    b = 0;
    printf("%2d %2d %4d %5d %5d\n", a, b, !a, a && b, a || b);
    a = 1;
    b = 1;
    printf("%2d %2d %4d %5d %5d\n", a, b, !a, a && b, a || b);
    a = 5;
    b = -3;
    printf("a = 5, b = -3 时：!a = %d，a && b = %d\n", !a, a && b);
    return 0;
}
