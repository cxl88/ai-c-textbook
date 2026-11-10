/* 程序名：cp_nest.c
   功能：核对任务三 课堂练习（if 嵌套）第 2、3 题和课堂活动 */
#include <stdio.h>

int main(void)
{
    int x, y, a, b;

    x = 5;
    y = 0;
    if (x > 0) if (x > 10) y = 1; else y = 2;
    printf("第2题 x=5：%d\n", y);
    x = -5;
    y = 0;
    if (x > 0) if (x > 10) y = 1; else y = 2;
    printf("第2题 x=-5：%d\n", y);
    x = 5;
    y = 0;
    if (x > 0)
    {
        if (x > 10)
        {
            y = 1;
        }
    }
    else
    {
        y = 2;
    }
    printf("第3题 x=5：%d\n", y);
    x = -5;
    y = 0;
    if (x > 0)
    {
        if (x > 10)
        {
            y = 1;
        }
    }
    else
    {
        y = 2;
    }
    printf("第3题 x=-5：%d\n", y);
    a = -1;
    b = 5;
    x = 0;
    if (a > 0) if (b > 0) x = 1; else x = 2;
    printf("课堂活动 a=-1,b=5：x = %d\n", x);
    return 0;
}
