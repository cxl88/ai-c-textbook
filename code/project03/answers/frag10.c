/* 实训巩固第 10 题核对：i 从 0 开始时循环执行几次 */
#include <stdio.h>

int main(void)
{
    int i, n;

    n = 0;
    i = 0;
    while (i <= 5)
    {
        n = n + 1;
        i = i + 1;
    }
    printf("循环体执行 %d 次，退出时 i = %d\n", n, i);
    return 0;
}
