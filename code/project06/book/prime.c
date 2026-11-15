/* 程序名：prime.c
   功能：输入一个正整数，判断它是不是素数（break） */
#include <stdio.h>

int main(void)
{
    int n, i;

    printf("请输入一个正整数：");
    scanf("%d", &n);
    for (i = 2; i < n; i++)            // 用 2～n-1 逐个去除 n
    {
        if (n % i == 0)                // 能整除，找到了因数
        {
            break;                     // 不必再试，提前结束循环
        }
    }
    if (i == n)                        // 一直试到 n-1，都不能整除
    {
        printf("%d 是素数\n", n);
    }
    else
    {
        printf("%d 不是素数\n", n);
    }
    return 0;
}
