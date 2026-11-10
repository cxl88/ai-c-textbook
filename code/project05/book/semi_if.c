/* 程序名：semi_if.c
   功能：错误示范——if 的条件后面多写了分号 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("电压（V）：");
    scanf("%f", &v);
    if (v > 21);                       // 多写了一个分号
    {
        printf("请注意过压！\n");
    }
    return 0;
}
