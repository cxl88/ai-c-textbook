/* 程序名：three_if.c
   功能：错误示范——三个独立的 if 语句，第二个条件照抄成 v <= 21（任务二 任务实施 小智提示） */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("请输入测得的电压（V）：");
    scanf("%f", &v);
    if (v < 15)
    {
        printf("欠压，请检查光伏组件！\n");
    }
    if (v <= 21)
    {
        printf("电压正常，组件稳定运行！\n");
    }
    if (v > 21)
    {
        printf("请注意过压！\n");
    }
    return 0;
}
