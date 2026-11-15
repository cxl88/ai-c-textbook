/* 程序名：harmonic.c
   功能：实训巩固第 15 题参考答案：求 1 + 1/2 + 1/3 + … + 1/n */
#include <stdio.h>

int main(void)
{
    int n, i;
    double s = 0;

    printf("请输入 n：");
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
    {
        s = s + 1.0 / i;               // 写成 1 / i 就成了整数除法
    }
    printf("和为 %.4f\n", s);
    return 0;
}
