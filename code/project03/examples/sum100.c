/* 程序名：sum100.c
   功能：用两种算法求 1+2+3+…+100 */
#include <stdio.h>

int main(void)
{
    int i, sum1, sum2;

    sum1 = 0;                       // 算法一：从 1 加到 100，逐个累加
    i = 1;
    while (i <= 100)
    {
        sum1 = sum1 + i;
        i = i + 1;
    }
    sum2 = (1 + 100) * 100 / 2;     // 算法二：高斯求和公式

    printf("算法一（逐个累加）：%d\n", sum1);
    printf("算法二（公式计算）：%d\n", sum2);
    return 0;
}
