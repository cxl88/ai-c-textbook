/* 程序名：hail.c
   功能：实训巩固第 17 题（挑战题）参考答案：冰雹猜想 */
#include <stdio.h>

int main(void)
{
    int n, steps = 0;

    printf("请输入一个正整数：");
    scanf("%d", &n);
    printf("%d", n);
    while (n != 1)
    {
        if (n % 2 == 0)
        {
            n = n / 2;
        }
        else
        {
            n = 3 * n + 1;
        }
        printf(" → %d", n);
        steps++;
    }
    printf("\n共变化 %d 步\n", steps);
    return 0;
}
