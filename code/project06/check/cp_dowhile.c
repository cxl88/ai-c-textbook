/* 程序名：cp_dowhile.c
   功能：核对任务一 课堂练习（do…while 语句）第 1、2 题 */
#include <stdio.h>

int main(void)
{
    int n, i;

    n = 0;
    do
    {
        n++;
    } while (n < 0);
    printf("第1题 do…while：n = %d\n", n);
    n = 0;
    while (n < 0)
    {
        n++;
    }
    printf("第1题 while：n = %d\n", n);
    printf("第2题：");
    i = 5;
    do
    {
        printf("%d ", i);
        i -= 2;
    } while (i > 0);
    printf("\n");
    return 0;
}
