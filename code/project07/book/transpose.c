/* 程序名：transpose.c
   功能：把 2 行 3 列的矩阵转置为 3 行 2 列 */
#include <stdio.h>

int main(void)
{
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int b[3][2];                       // 转置后的矩阵
    int i, j;

    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < 3; j++)
        {
            b[j][i] = a[i][j];         // 行列互换
        }
    }
    for (i = 0; i < 3; i++)
    {
        for (j = 0; j < 2; j++)
        {
            printf("%3d", b[i][j]);
        }
        printf("\n");
    }
    return 0;
}
