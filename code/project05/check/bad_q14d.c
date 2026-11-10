/* 程序名：bad_q14d.c
   功能：实训巩固第 14 题核对：改正第 1、2、3 处错误后再编译（只编译） */
#include <stdio.h>

int main(void)
{
    float t;                           // 室内温度（℃）

    printf("室内温度（℃）：");
    scanf("%f", &t);
    if (t > 26)
    {
        printf("空调：制冷\n");
    }
    else if (t <= 18)
    {
        printf("空调：制热\n");
    }
    else
    {
        printf("空调：待机\n")
    }
    return 0;
}
