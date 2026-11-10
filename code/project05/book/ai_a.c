/* 程序名：ai_a.c
   功能：AI 给出的写法①（四个分支并列） */
#include <stdio.h>

int main(void)
{
    float v;

    printf("请输入测得的电压（V）：");
    scanf("%f", &v);
    if (v < 15)
    {
        printf("欠压，请检查光伏组件！\n");
    }
    else if (v >= 15 && v <= 21)
    {
        printf("电压正常，组件稳定运行！\n");
    }
    else if (v > 21 && v <= 24)
    {
        printf("请注意过压！\n");
        printf("及时核查组件与线路！\n");
    }
    else
    {
        printf("请注意过压！\n");
        printf("紧急告警，立即停机保护！\n");
    }
    return 0;
}
