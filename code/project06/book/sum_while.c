/* 程序名：sum_while.c
   功能：用 while 语句求 1+2+3+…+100 */
#include <stdio.h>

int main(void)
{
    int i, sum;

    sum = 0;                           // 和的初值为 0
    i = 1;                             // 循环变量 i 的初值为 1
    while (i <= 100)                   // 循环条件：i 不超过 100
    {
        sum = sum + i;                 // 把 i 加到 sum 中
        i++;                           // i 增加 1
    }
    printf("1+2+…+100 = %d\n", sum);
    return 0;
}
