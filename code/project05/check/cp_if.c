/* 程序名：cp_if.c
   功能：核对任务一 课堂练习（单分支 if 语句）第 1 题 */
#include <stdio.h>

int main(void)
{
    int x;

    x = 5;
    printf("x 为 5 时：");
    if (x > 3) printf("A");
    printf("B");
    printf("\n");
    x = 1;
    printf("x 为 1 时：");
    if (x > 3) printf("A");
    printf("B");
    printf("\n");
    return 0;
}
