/* 程序名：chicken.c
   功能：百钱买百鸡（穷举法） */
#include <stdio.h>

int main(void)
{
    int x, y, z;                       // 公鸡、母鸡、小鸡的只数

    printf("公鸡  母鸡  小鸡\n");
    for (x = 0; x <= 20; x++)          // 公鸡最多 100÷5 = 20 只
    {
        for (y = 0; y <= 33; y++)      // 母鸡最多 100÷3，取 33 只
        {
            z = 100 - x - y;           // 小鸡的只数随之确定
            if (z % 3 == 0 && 5 * x + 3 * y + z / 3 == 100)
            {
                printf("%4d%6d%6d\n", x, y, z);
            }
        }
    }
    return 0;
}
