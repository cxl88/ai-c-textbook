/* 程序名：narc.c
   功能：实训巩固第 16 题参考答案：输出所有的水仙花数 */
#include <stdio.h>

int main(void)
{
    int n, a, b, c;                    // a、b、c：百位、十位、个位

    for (n = 100; n <= 999; n++)
    {
        a = n / 100;
        b = n / 10 % 10;
        c = n % 10;
        if (a * a * a + b * b * b + c * c * c == n)
        {
            printf("%d ", n);
        }
    }
    printf("\n");
    return 0;
}
