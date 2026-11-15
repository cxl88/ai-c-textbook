/* 程序名：cp_for.c
   功能：核对任务二 课堂练习（for 语句）第 1、2 题 */
#include <stdio.h>

int main(void)
{
    int i, n = 0;

    printf("第1题：");
    for (i = 1; i <= 10; i += 3)
    {
        printf("%d ", i);
        n++;
    }
    printf("\n循环 %d 次，结束后 i = %d\n", n, i);
    printf("第2题：");
    for (i = 10; i >= 1; i--)
    {
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
