/* 程序名：mul9.c
   功能：输出九九乘法表 */
#include <stdio.h>

int main(void)
{
    int i, j;

    for (i = 1; i <= 9; i++)           // 外层：第 i 行
    {
        for (j = 1; j <= i; j++)       // 内层：第 i 行有 i 个算式
        {
            printf("%d*%d=%-3d", j, i, i * j);
        }
        printf("\n");
    }
    return 0;
}
