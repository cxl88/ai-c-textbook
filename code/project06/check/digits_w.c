/* 程序名：digits_w.c
   功能：把例6-6 改用 while 语句，输入 0 时的结果 */
#include <stdio.h>

int main(void)
{
    int n, count = 0;

    printf("请输入一个整数：");
    scanf("%d", &n);
    printf("%d 是", n);
    while (n != 0)
    {
        n = n / 10;
        count++;
    }
    printf(" %d 位数\n", count);
    return 0;
}
