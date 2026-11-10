/* 程序名：mut_volt2.c
   功能：课堂验收（任务二）：把 v < 15 改成 v <= 15 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    /* 输入 */
    printf("请输入测得的电压（V）：");
    scanf("%f", &v);

    /* 处理和输出：三种状态只输出一种 */
    if (v <= 15)
    {
        printf("欠压，请检查光伏组件！\n");
    }
    else if (v <= 21)                  // 走到这里，说明 v≥15
    {
        printf("电压正常，组件稳定运行！\n");
    }
    else                               // 剩下的情况：v＞21
    {
        printf("请注意过压！\n");
    }
    return 0;
}
