/* 程序名：rel.c
   功能：输出关系表达式的值（成立为 1，不成立为 0） */
#include <stdio.h>

int main(void)
{
    float v = 22;                      // 测得的电压（V）
    char c = 'Y';                      // 状态字母

    printf("v > 21     的值：%d\n", v > 21);
    printf("v <= 21    的值：%d\n", v <= 21);
    printf("v - 3 > 18 的值：%d\n", v - 3 > 18);
    printf("c == 'Y'   的值：%d\n", c == 'Y');
    printf("c != 'N'   的值：%d\n", c != 'N');
    printf("'A' < 'a'  的值：%d\n", 'A' < 'a');
    return 0;
}
