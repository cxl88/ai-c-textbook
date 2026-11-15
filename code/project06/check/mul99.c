/* 程序名：mul99.c
   功能：任务二 课堂练习（循环嵌套）第 4 题参考答案：输出 9 行 9 列的乘法表 */
#include <stdio.h>

int main(void)
{
    int i, j;

    for (i = 1; i <= 9; i++)
    {
        for (j = 1; j <= 9; j++)
        {
            printf("%d*%d=%-3d", j, i, i * j);
        }
        printf("\n");
    }
    return 0;
}
