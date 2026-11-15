/* 程序名：even_sum.c
   功能：任务一 课堂练习（while 语句）第 4 题参考答案：求 2+4+6+…+100 */
#include <stdio.h>

int main(void)
{
    int i = 2, sum = 0;

    while (i <= 100)
    {
        sum = sum + i;
        i = i + 2;
    }
    printf("2+4+6+…+100 = %d\n", sum);
    return 0;
}
