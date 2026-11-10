/* 程序名：max3.c
   功能：实训巩固第 16 题参考答案：输出三个整数中最大的数 */
#include <stdio.h>

int main(void)
{
    int a, b, c, max;

    printf("请输入三个整数（用空格隔开）：");
    scanf("%d%d%d", &a, &b, &c);
    max = a > b ? a : b;               // 先取 a、b 中较大的
    if (c > max)                       // 再与 c 比较
    {
        max = c;
    }
    printf("最大的数：%d\n", max);
    return 0;
}
