/* 程序名：skip3.c
   功能：输出 1～20 中不能被 3 整除的数（continue） */
#include <stdio.h>

int main(void)
{
    int i;

    for (i = 1; i <= 20; i++)
    {
        if (i % 3 == 0)                // 能被 3 整除
        {
            continue;                  // 跳过本次循环中后面的输出
        }
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
