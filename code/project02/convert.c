#include <stdio.h>

int main(void)
{
    int a = 24.9;               // 小数存入 int：小数部分被直接舍去
    double b = 7 / 2;           // 两个整数相除：先得到整数 3
    double c = (double)7 / 2;   // 先把 7 转成 7.0，再相除
    double d = 7 / 2.0;         // 有一个是小数，就按小数除法计算

    printf("a = %d\n", a);
    printf("b = %.1f\n", b);
    printf("c = %.1f\n", c);
    printf("d = %.1f\n", d);
    return 0;
}
