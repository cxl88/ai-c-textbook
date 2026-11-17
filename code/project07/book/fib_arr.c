/* 程序名：fib_arr.c
   功能：用数组求兔子数列（斐波那契数列）的前 20 项，每行 5 个 */
#include <stdio.h>

int main(void)
{
    int f[20] = {1, 1};                // 前两项为 1，其余先为 0
    int i;

    for (i = 2; i < 20; i++)
    {
        f[i] = f[i - 1] + f[i - 2];    // 每一项等于前两项之和
    }
    for (i = 0; i < 20; i++)
    {
        printf("%8d", f[i]);
        if ((i + 1) % 5 == 0)          // 每输出 5 个换行
        {
            printf("\n");
        }
    }
    printf("第12项是%d\n", f[11]);
    return 0;
}
