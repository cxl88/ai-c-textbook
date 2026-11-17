/* 程序名：cp_q15.c
   功能：实训巩固第 15 题参考答案：统计正数、负数和零的个数 */
#include <stdio.h>

int main(void)
{
    int a[10];
    int i, pos = 0, neg = 0, zero = 0;

    printf("请输入10个整数：");
    for (i = 0; i < 10; i++)
    {
        scanf("%d", &a[i]);
    }
    for (i = 0; i < 10; i++)
    {
        if (a[i] > 0)
        {
            pos++;
        }
        else if (a[i] < 0)
        {
            neg++;
        }
        else
        {
            zero++;
        }
    }
    printf("正数%d个，负数%d个，零%d个\n", pos, neg, zero);
    return 0;
}
