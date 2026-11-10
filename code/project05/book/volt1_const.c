/* 程序名：volt1_const.c
   功能：用符号常量表示正常区间的下限和上限（任务一 技能训练 2） */
#include <stdio.h>
#define VMIN 15                        // 正常区间下限（V）
#define VMAX 21                        // 正常区间上限（V）

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("请输入测得的电压（V）：");
    scanf("%f", &v);
    if (v < VMIN || v > VMAX)
    {
        printf("电压异常，请检查光伏组件！\n");
        printf("（正常区间：%d～%d V）\n", VMIN, VMAX);
    }
    return 0;
}
