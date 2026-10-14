/* 实训巩固第 9 题参考：求 1×2×3×…×10 */
#include <stdio.h>

int main(void)
{
    int i, p;

    p = 1;                  // 累乘的初值是 1，不能是 0
    i = 1;
    while (i <= 10)
    {
        p = p * i;
        i = i + 1;
    }
    printf("1×2×…×10 = %d\n", p);
    return 0;
}
