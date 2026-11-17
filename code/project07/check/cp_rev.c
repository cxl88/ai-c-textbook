/* 程序名：cp_rev.c
   功能：课堂练习参考答案：输入 5 个整数，逆序输出 */
#include <stdio.h>

int main(void)
{
    int a[5];
    int i;

    printf("请输入5个整数：");
    for (i = 0; i < 5; i++)
    {
        scanf("%d", &a[i]);
    }
    for (i = 4; i >= 0; i--)
    {
        printf("%d ", a[i]);
    }
    printf("\n");
    return 0;
}
