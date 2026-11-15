/* 程序名：cp_q13.c
   功能：核对实训巩固第 13 题 */
#include <stdio.h>

int main(void)
{
    int i, j;

    for (i = 1; i <= 3; i++)
    {
        for (j = 1; j <= 3; j++)
        {
            if (j > i)
            {
                break;
            }
            printf("%d", i * j);
        }
        printf("\n");
    }
    return 0;
}
