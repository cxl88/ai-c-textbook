/* 程序名：init2.c
   功能：二维数组初始化的几种情况 */
#include <stdio.h>

int main(void)
{
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};  // 分行赋初值
    int b[2][3] = {1, 2, 3, 4, 5, 6};      // 不分行，按行的顺序赋初值
    int c[2][3] = {{1}, {4, 5}};           // 部分赋初值，其余为 0
    int i;

    printf("a       b       c\n");
    for (i = 0; i < 2; i++)            // 每次输出三个数组的第 i 行
    {
        printf("%d %d %d   ", a[i][0], a[i][1], a[i][2]);
        printf("%d %d %d   ", b[i][0], b[i][1], b[i][2]);
        printf("%d %d %d\n", c[i][0], c[i][1], c[i][2]);
    }
    return 0;
}
