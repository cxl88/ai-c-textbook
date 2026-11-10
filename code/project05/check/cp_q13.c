/* 程序名：cp_q13.c
   功能：核对实训巩固第 13 题：x 分别为 5、15、25 */
#include <stdio.h>

int main(void)
{
    int x;

    printf("x：");
    scanf("%d", &x);
    if (x > 10)
    {
        if (x > 20)
        {
            printf("A\n");
        }
        else
        {
            printf("B\n");
        }
    }
    else
    {
        printf("C\n");
    }
    return 0;
}
