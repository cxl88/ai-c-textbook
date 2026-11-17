/* 程序名：fix_q14.c
   功能：实训巩固第 14 题改正后的程序 */
#include <stdio.h>
#define N 5

int main(void)
{
    float r[N], sum = 0, avg;          // 阻值、阻值之和、平均值
    int i;

    for (i = 0; i < N; i++)
    {
        printf("第%d个电阻的阻值（Ω）：", i + 1);
        scanf("%f", &r[i]);
        sum = sum + r[i];
    }
    avg = sum / N;
    printf("平均值：%.1f Ω\n", avg);
    for (i = 0; i < N; i++)
    {
        if (r[i] > avg)
        {
            printf("%.1f ", r[i]);
        }
    }
    printf("\n");
    return 0;
}
