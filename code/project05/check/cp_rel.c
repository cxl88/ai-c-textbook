/* 程序名：cp_rel.c
   功能：核对任务一 课堂练习（关系运算符）第 1、2、4 题 */
#include <stdio.h>

int main(void)
{
    int a = 3, b = 5, x;

    printf("第1题：%d %d %d %d %d\n", a > b, a != b, a + 2 == b, b - a >= 2, 'a' > 'B');
    printf("第2题：%d\n", 10 > 5 > 2);
    x = 3 > 2;
    printf("第4题：x = %d\n", x);
    return 0;
}
