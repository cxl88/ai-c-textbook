/* 程序名：digits.c
   功能：输入一个整数，统计它是几位数（do…while） */
#include <stdio.h>

int main(void)
{
    int n, count = 0;                  // count：位数

    printf("请输入一个整数：");
    scanf("%d", &n);
    printf("%d 是", n);
    do
    {
        n = n / 10;                    // 去掉最后一位
        count++;                       // 位数加 1
    } while (n != 0);                  // 还有数字，就继续
    printf(" %d 位数\n", count);
    return 0;
}
