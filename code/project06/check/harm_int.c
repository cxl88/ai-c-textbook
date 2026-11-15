/* 程序名：harm_int.c
   功能：实训巩固第 15 题核对：误写成 1 / i 的结果 */
#include <stdio.h>

int main(void)
{
    int n, i;
    double s = 0;

    printf("请输入 n：");
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
    {
        s = s + 1 / i;
    }
    printf("和为 %.4f\n", s);
    return 0;
}
