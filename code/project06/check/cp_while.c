/* 程序名：cp_while.c
   功能：核对任务一 课堂练习（while 语句）第 1、2 题 */
#include <stdio.h>

int main(void)
{
    int i, s, n;

    i = 1;
    s = 0;
    while (i < 100)
    {
        s = s + i;
        i++;
    }
    printf("第1题：i = %d，s = %d\n", i, s);
    i = 10;
    n = 0;
    while (i > 0)
    {
        i = i - 3;
        n++;
    }
    printf("第2题：循环 %d 次，结束后 i = %d\n", n, i);
    return 0;
}
