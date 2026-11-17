/* 程序名：cp_q13.c
   功能：实训巩固第 13 题（读程序） */
#include <stdio.h>

int main(void)
{
    int a[6] = {3, 8, 2, 9, 5, 1};
    int i, s = 0, k = 0;

    for (i = 0; i < 6; i++)
    {
        if (a[i] % 2 == 1)
        {
            s = s + a[i];
        }
        if (a[i] > a[k])
        {
            k = i;
        }
    }
    printf("%d %d %d\n", s, k, a[k]);
    return 0;
}
