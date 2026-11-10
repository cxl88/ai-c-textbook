/* 程序名：mut_volt1.c
   功能：课堂验收（任务一）：把 v > 21 改成 v >= 21 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    /* 输入 */
    printf("请输入测得的电压（V）：");
    scanf("%f", &v);

    /* 处理和输出：低于 15 V 或高于 21 V 时提示异常 */
    if (v < 15 || v >= 21)
    {
        printf("电压异常，请检查光伏组件！\n");
    }
    return 0;
}
