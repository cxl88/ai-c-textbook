/* 程序名：fib.c
   功能：输出斐波那契数列（兔子数列）的前 20 项，每行 5 个 */
#include <stdio.h>

int main(void)
{
    int f1 = 1, f2 = 1, f, i;          // f1、f2：前两项

    printf("%8d%8d", f1, f2);          // 先输出第 1、2 项
    for (i = 3; i <= 20; i++)
    {
        f = f1 + f2;                   // 新的一项等于前两项之和
        printf("%8d", f);
        if (i % 5 == 0)                // 每输出 5 个换一行
        {
            printf("\n");
        }
        f1 = f2;                       // 向后“递推”一项
        f2 = f;
    }
    return 0;
}
