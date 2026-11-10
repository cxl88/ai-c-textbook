/* 程序名：volt3b.c
   功能：紧急过压时输出超出 24 V 的数值（任务三 技能训练 2） */
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
    else if (v <= 21)
    {
        printf("电压正常，组件稳定运行！\n");
    }
    else
    {
        printf("请注意过压！\n");
        if (v <= 24)
        {
            printf("及时核查组件与线路！\n");
        }
        else
        {
            printf("紧急告警，立即停机保护！\n");
            printf("超出 24 V 共 %.1f V。\n", v - 24);
        }
    }
    return 0;
}
