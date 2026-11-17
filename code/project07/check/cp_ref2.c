/* 程序名：cp_ref2.c
   功能：核对课堂练习：二维数组的引用 */
#include <stdio.h>

int main(void)
{
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int m[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int i, j, sum = 0, d = 0;

    for (j = 0; j < 3; j++)
    {
        printf("%d ", a[1][j]);
    }
    printf("\n");
    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < 3; j++)
        {
            sum = sum + a[i][j];
        }
    }
    printf("sum=%d\n", sum);
    for (i = 0; i < 3; i++)
    {
        printf("%d ", m[i][i]);
        d = d + m[i][i];
    }
    printf("\n对角线之和=%d\n", d);
    return 0;
}
