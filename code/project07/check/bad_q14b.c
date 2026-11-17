/* 程序名：bad_q14b.c
   功能：核对实训巩固第 14 题：改掉前两处错误后，编译器还能发现什么 */
#include <stdio.h>

int main(void)
{
    float r[5], sum, avg;              // 阻值、阻值之和、平均值
    int i;

    for (i = 1; i <= 5; i++)
    {
        printf("第%d个电阻的阻值（Ω）：", i);
        scanf("%f", &r[i]);
        sum = sum + r[i];
    }
    avg = sum / 5;
    printf("平均值：%.1f Ω\n", avg);
    for (i = 0; i < 5; i++)
    {
        if (r[i] > avg)
        {
            printf("%.1f ", r[i]);
        }
    }
    printf("\n");
    return 0;
}
