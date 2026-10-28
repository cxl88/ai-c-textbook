/* 实训巩固第 8 题核对：判断一个整数是奇数还是偶数 */
#include <stdio.h>

int main(void)
{
    int n;

    printf("请输入一个整数：");
    scanf("%d", &n);
    if (n % 2 == 0)
    {
        printf("%d 是偶数\n", n);
    }
    else
    {
        printf("%d 是奇数\n", n);
    }
    return 0;
}
