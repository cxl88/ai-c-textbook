/* 程序名：cp_nz3.c
   功能：任务三 课堂练习（典型示例）第 3 题：去掉 z % 3 == 0 后的百钱买百鸡 */
#include <stdio.h>

int main(void)
{
    int x, y, z;                       // 公鸡、母鸡、小鸡的只数

    printf("公鸡  母鸡  小鸡\n");
    for (x = 0; x <= 20; x++)
    {
        for (y = 0; y <= 33; y++)
        {
            z = 100 - x - y;
            if (5 * x + 3 * y + z / 3 == 100)
            {
                printf("%4d%6d%6d\n", x, y, z);
            }
        }
    }
    return 0;
}
