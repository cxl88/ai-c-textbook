/* 程序名：bad_q14.c
   功能：根据室内温度决定空调的工作方式 */
#include <stdio.h>

int main(void)
{
    float t;                           // 室内温度（℃）

    printf("室内温度（℃）：");
    scanf("%f", &t);
    if t > 26
    {
        printf("空调：制冷\n");
    }
    else if (t =< 18)
    {
        printf("空调：制热\n");
    }
    elseif
    {
        printf("空调：待机\n")
    }
    return 0;
}
