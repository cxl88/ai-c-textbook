/* 程序名：cp_trans3.c
   功能：课堂练习参考答案：3 行 3 列的矩阵转置 */
#include <stdio.h>

int main(void)
{
    int a[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int b[3][3];
    int i, j;

    for (i = 0; i < 3; i++)
    {
        for (j = 0; j < 3; j++)
        {
            b[j][i] = a[i][j];
        }
    }
    for (i = 0; i < 3; i++)
    {
        for (j = 0; j < 3; j++)
        {
            printf("%3d", b[i][j]);
        }
        printf("\n");
    }
    return 0;
}
