/* 程序名：grid.c
   功能：用循环嵌套输出 3 行 4 列灯阵的灯位编号 */
#include <stdio.h>

int main(void)
{
    int row, col;                      // 行号、列号

    for (row = 1; row <= 3; row++)      // 外层循环：第 1～3 行
    {
        for (col = 1; col <= 4; col++)  // 内层循环：第 1～4 列
        {
            printf("%d-%d  ", row, col);
        }
        printf("\n");                   // 一行输出完，换行
    }
    return 0;
}
