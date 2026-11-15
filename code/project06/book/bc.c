/* 程序名：bc.c
   功能：比较 break 和 continue */
#include <stdio.h>

int main(void)
{
    int i;

    printf("用 break：   ");
    for (i = 1; i <= 10; i++)
    {
        if (i % 4 == 0)
        {
            break;                     // 遇到 4 的倍数，结束整个循环
        }
        printf("%d ", i);
    }

    printf("\n用 continue：");
    for (i = 1; i <= 10; i++)
    {
        if (i % 4 == 0)
        {
            continue;                  // 遇到 4 的倍数，只跳过这一次
        }
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
