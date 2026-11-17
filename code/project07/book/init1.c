/* 程序名：init1.c
   功能：一维数组初始化的几种情况 */
#include <stdio.h>

int main(void)
{
    int a[5] = {1, 2, 3, 4, 5};        // 全部元素赋初值
    int b[5] = {1, 2};                 // 部分元素赋初值，其余为 0
    int c[5] = {0};                    // 全部元素为 0
    int d[] = {7, 8, 9};               // 省略长度，由初值个数确定为 3
    int i;

    printf("下标   a   b   c\n");
    for (i = 0; i < 5; i++)
    {
        printf("%4d%4d%4d%4d\n", i, a[i], b[i], c[i]);
    }
    printf("d：%d %d %d\n", d[0], d[1], d[2]);
    return 0;
}
