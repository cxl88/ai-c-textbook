/* 程序名：sum_do.c
   功能：用 do…while 语句求 1+2+3+…+100 */
#include <stdio.h>

int main(void)
{
    int i, sum;

    sum = 0;
    i = 1;
    do
    {
        sum = sum + i;
        i++;
    } while (i <= 100);                // 末尾的分号不能少
    printf("1+2+…+100 = %d\n", sum);
    return 0;
}
