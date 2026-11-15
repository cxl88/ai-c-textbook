/* 程序名：sum_n.c
   功能：输入 n，分别用 while 和 do…while 求 1+2+…+n */
#include <stdio.h>

int main(void)
{
    int n, i, sum1, sum2;

    printf("请输入 n：");
    scanf("%d", &n);

    sum1 = 0;                          // while：先判断，后执行
    i = 1;
    while (i <= n)
    {
        sum1 = sum1 + i;
        i++;
    }

    sum2 = 0;                          // do…while：先执行，后判断
    i = 1;
    do
    {
        sum2 = sum2 + i;
        i++;
    } while (i <= n);

    printf("用 while 求得：%d\n", sum1);
    printf("用 do…while 求得：%d\n", sum2);
    return 0;
}
