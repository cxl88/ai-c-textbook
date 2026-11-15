/* 程序名：fact.c
   功能：输入 n（1～12），用 for 语句求 n! = 1×2×…×n */
#include <stdio.h>

int main(void)
{
    int n, i, f = 1;                   // f：积，初值为 1

    printf("请输入 n（1～12）：");
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
    {
        f = f * i;                     // 累乘
    }
    printf("%d! = %d\n", n, f);
    return 0;
}
