/* 程序名：volt2b.c
   功能：欠压时增加“组件进入待机”的提示（任务二 技能训练 2） */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("请输入测得的电压（V）：");
    scanf("%f", &v);
    if (v < 15)
    {
        printf("欠压，请检查光伏组件！\n");
        printf("组件进入待机。\n");
    }
    else if (v <= 21)
    {
        printf("电压正常，组件稳定运行！\n");
    }
    else
    {
        printf("请注意过压！\n");
    }
    return 0;
}
