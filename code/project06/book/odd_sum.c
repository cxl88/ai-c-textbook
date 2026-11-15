/* 程序名：odd_sum.c
   功能：用 while 语句求 1+3+5+…+99（任务一 技能训练 1） */
#include <stdio.h>

int main(void)
{
    int i, sum;

    sum = 0;
    i = 1;                             // ① 循环变量的初值
    while (i <= 99)                    // ② 循环条件
    {
        sum = sum + i;
        i = i + 2;                     // ③ 每次加 2
    }
    printf("1+3+5+…+99 = %d\n", sum);
    return 0;
}
