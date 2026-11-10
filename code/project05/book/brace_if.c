/* 程序名：brace_if.c
   功能：错误示范——if 后面有两条语句，却没有加花括号 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("电压（V）：");
    scanf("%f", &v);
    if (v > 21)
        printf("请注意过压！\n");
        printf("及时核查组件与线路！\n");
    return 0;
}
