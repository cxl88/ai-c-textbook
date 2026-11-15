/* 程序名：cp_sum3.c
   功能：任务二 课堂练习（for 语句）第 4 题：求 1～100 中所有 3 的倍数之和 */
#include <stdio.h>

int main(void)
{
    int i, sum = 0;

    for (i = 3; i <= 100; i = i + 3)   // i 从 3 开始，每次加 3
    {
        sum = sum + i;
    }
    printf("1～100 中 3 的倍数之和：%d\n", sum);
    return 0;
}
