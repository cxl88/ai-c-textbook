/* 程序名：leap5.c
   功能：任务二 课堂练习（if…else 语句）第 3 题参考答案：判断闰年 */
#include <stdio.h>

int main(void)
{
    int year;

    printf("年份：");
    scanf("%d", &year);
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)
    {
        printf("%d 年是闰年。\n", year);
    }
    else
    {
        printf("%d 年不是闰年。\n", year);
    }
    return 0;
}
