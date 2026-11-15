/* 程序名：triangle.c
   功能：输入行数 n，输出 n 行的星号直角三角形（任务二 技能训练 3） */
#include <stdio.h>

int main(void)
{
    int n, i, j;

    printf("请输入行数：");
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
    {
        for (j = 1; j <= i; j++)       // 第 i 行输出 i 个 *
        {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}
