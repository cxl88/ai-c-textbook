/* 程序名：bad_q14.c
   功能：输入 5 次电压测量值，求平均值 */
#include <stdio.h>

int main(void)
{
    int i;
    float v, sum;

    for (i = 1, i <= 5, i++)
    {
        printf("第%d次测量值（V）：", i);
        scanf("%f", v);
        sum = sum + v
    }
    printf("平均电压：%.2f V\n", sum / 5);
    return 0;
}
