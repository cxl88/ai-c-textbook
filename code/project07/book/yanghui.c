/* 程序名：yanghui.c
   功能：输出杨辉三角的前 10 行 */
#include <stdio.h>

int main(void)
{
    int a[10][10];
    int i, j;

    for (i = 0; i < 10; i++)
    {
        a[i][0] = 1;                   // 每行第一个数是 1
        a[i][i] = 1;                   // 每行最后一个数是 1
        for (j = 1; j < i; j++)        // 中间的数等于它“肩上”两数之和
        {
            a[i][j] = a[i - 1][j - 1] + a[i - 1][j];
        }
    }
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j <= i; j++)
        {
            printf("%4d", a[i][j]);
        }
        printf("\n");
    }
    return 0;
}
