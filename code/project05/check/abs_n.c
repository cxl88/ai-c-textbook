/* 程序名：abs_n.c
   功能：任务一 课堂练习（单分支 if 语句）第 4 题参考答案：求绝对值 */
#include <stdio.h>

int main(void)
{
    int n;

    printf("请输入一个整数：");
    scanf("%d", &n);
    if (n < 0)
    {
        n = -n;
    }
    printf("绝对值：%d\n", n);
    return 0;
}
