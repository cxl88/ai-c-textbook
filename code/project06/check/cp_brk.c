/* 程序名：cp_brk.c
   功能：核对任务三 课堂练习（break 与 continue）第 1、2、4 题 */
#include <stdio.h>

int main(void)
{
    int i, j, n;

    printf("第1题 break：");
    for (i = 1; i <= 10; i++)
    {
        if (i % 3 == 0)
        {
            break;
        }
        printf("%d ", i);
    }
    printf("\n第1题 continue：");
    for (i = 1; i <= 10; i++)
    {
        if (i % 3 == 0)
        {
            continue;
        }
        printf("%d ", i);
    }
    i = 0;
    n = 0;
    while (1)
    {
        i++;
        n++;
        if (i == 5)
        {
            break;
        }
    }
    printf("\n第2题：循环体执行 %d 次，结束后 i = %d\n", n, i);
    printf("第4题：");
    for (i = 1; i <= 3; i++)
    {
        for (j = 1; j <= 3; j++)
        {
            if (j == 2)
            {
                break;
            }
            printf("%d%d ", i, j);
        }
    }
    printf("\n");
    return 0;
}
