/* 程序名：sum_for.c
   功能：用 for 语句求 1+2+3+…+100 */
#include <stdio.h>

int main(void)
{
    int i, sum = 0;

    for (i = 1; i <= 100; i++)         // 初值、条件、修改写在一起
    {
        sum = sum + i;                 // 循环体
    }
    printf("1+2+…+100 = %d\n", sum);
    printf("循环结束后，i = %d\n", i);
    return 0;
}
