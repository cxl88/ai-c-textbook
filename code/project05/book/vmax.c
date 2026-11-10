/* 程序名：vmax.c
   功能：用条件运算符求两次测量中较高的电压 */
#include <stdio.h>

int main(void)
{
    float v1, v2, vmax;                // 两次测得的电压、较高的电压（V）

    printf("两次测得的电压（V，用空格隔开）：");
    scanf("%f%f", &v1, &v2);
    vmax = v1 > v2 ? v1 : v2;          // v1 大取 v1，否则取 v2
    printf("较高的电压：%.1f V\n", vmax);
    return 0;
}
