/* 程序名：fix_q14.c
   功能：实训巩固第 14 题参考答案：改正后的程序 */
#include <stdio.h>

int main(void)
{
    int i;
    float v, sum = 0;

    for (i = 1; i <= 5; i++)
    {
        printf("第%d次测量值（V）：", i);
        scanf("%f", &v);
        sum = sum + v;
    }
    printf("平均电压：%.2f V\n", sum / 5);
    return 0;
}
