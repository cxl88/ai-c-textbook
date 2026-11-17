/* 程序名：lamp_arr.c
   功能：用二维数组存放 3 行 4 列灯阵的状态码，找出异常的灯 */
#include <stdio.h>

int main(void)
{
    int lamp[3][4] = {{1, 1, 2, 1}, {1, 0, 1, 1}, {2, 1, 1, 1}};
    int i, j;                          // 行下标、列下标

    for (i = 0; i < 3; i++)            // 外层循环：逐行
    {
        for (j = 0; j < 4; j++)        // 内层循环：逐列
        {
            if (lamp[i][j] == 0)
            {
                printf("第%d行第%d列：短路不亮\n", i + 1, j + 1);
            }
            else if (lamp[i][j] == 2)
            {
                printf("第%d行第%d列：闪烁异常\n", i + 1, j + 1);
            }
        }
    }
    return 0;
}
