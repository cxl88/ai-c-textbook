/* 程序名：bad_q14d.c
   功能：实训巩固第 14 题核对：改正第 1、2、3 处错误后再编译（只编译） */
#include <stdio.h>

int main(void)
{
    int i;
    float v, sum;

    for (i = 1; i <= 5; i++)
    {
        printf("第%d次测量值（V）：", i);
        scanf("%f", &v);
        sum = sum + v;
    }
    printf("平均电压：%.2f V\n", sum / 5);
    return 0;
}
