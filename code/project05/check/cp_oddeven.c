/* 程序名：cp_oddeven.c
   功能：核对任务二 课堂练习（if…else 语句）第 1 题 */
#include <stdio.h>

int main(void)
{
    int x;

    x = 7;
    if (x % 2 == 0) printf("偶数"); else printf("奇数");
    printf("\n");
    x = 10;
    if (x % 2 == 0) printf("偶数"); else printf("奇数");
    printf("\n");
    return 0;
}
