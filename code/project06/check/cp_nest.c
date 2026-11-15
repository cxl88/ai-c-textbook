/* 程序名：cp_nest.c
   功能：核对任务二 课堂练习（循环嵌套）第 1、2、3 题 */
#include <stdio.h>

int main(void)
{
    int i, j, n = 0;

    for (i = 1; i <= 3; i++)
    {
        for (j = 1; j <= 5; j++)
        {
            n++;
        }
    }
    printf("第1题：输出 %d 个 *\n", n);
    printf("第2题：\n");
    for (i = 1; i <= 3; i++)
    {
        for (j = 1; j <= i; j++)
        {
            printf("%d", j);
        }
        printf("\n");
    }
    printf("第3题：\n");
    for (i = 1; i <= 3; i++)
    {
        for (i = 1; i <= 4; i++)
        {
            printf("*");
        }
        printf("\n");
    }
    printf("第3题结束后 i = %d\n", i);
    return 0;
}
