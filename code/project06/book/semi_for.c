/* 程序名：semi_for.c
   功能：错误示范——for 的圆括号后面多写了分号 */
#include <stdio.h>

int main(void)
{
    int i, sum = 0;

    for (i = 1; i <= 100; i++);        // 多写了一个分号
    {
        sum = sum + i;
    }
    printf("1+2+…+100 = %d\n", sum);
    return 0;
}
