#include <stdio.h>

int main(void)
{
    printf("7 + 2 = %d\n", 7 + 2);
    printf("7 - 2 = %d\n", 7 - 2);
    printf("7 * 2 = %d\n", 7 * 2);
    printf("7 / 2 = %d\n", 7 / 2);          // 整数相除，结果是整数
    printf("7.0 / 2 = %.1f\n", 7.0 / 2);    // 有实数参加，结果是实数
    printf("7 %% 2 = %d\n", 7 % 2);         // 7 除以 2 的余数
    printf("-7 / 2 = %d\n", -7 / 2);        // 小数部分直接舍去
    printf("-7 %% 2 = %d\n", -7 % 2);       // 余数与被除数同号
    return 0;
}
