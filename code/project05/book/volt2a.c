/* 程序名：volt2a.c
   功能：电压正常时也给出提示（任务二 第一处不足） */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("请输入测得的电压（V）：");
    scanf("%f", &v);
    if (v >= 15 && v <= 21)
    {
        printf("电压正常，组件稳定运行！\n");
    }
    else
    {
        printf("电压异常，请检查光伏组件！\n");
    }
    return 0;
}
