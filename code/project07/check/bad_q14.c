/* 程序名：bad_q14.c
   功能：输入 5 个电阻的阻值，输出平均值和大于平均值的阻值 */
#include <stdio.h>

int main(void)
{
    int n = 5;
    float r[n], sum, avg;              // 阻值、阻值之和、平均值
    int i;

    for (i = 1; i <= 5; i++)
    {
        printf("第%d个电阻的阻值（Ω）：", i);
        scanf("%f", r[i]);
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
