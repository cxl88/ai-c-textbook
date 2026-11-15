/* 程序名：cp_chick.c
   功能：核对例6-17：两层循环与三层循环（每种都试 0～100）各试多少次 */
#include <stdio.h>

int main(void)
{
    int x, y, z;
    long t2 = 0, t3 = 0;
    int s2 = 0, s3 = 0;

    for (x = 0; x <= 20; x++)
    {
        for (y = 0; y <= 33; y++)
        {
            t2++;
            z = 100 - x - y;
            if (z % 3 == 0 && 5 * x + 3 * y + z / 3 == 100)
            {
                s2++;
            }
        }
    }
    for (x = 0; x <= 100; x++)
    {
        for (y = 0; y <= 100; y++)
        {
            for (z = 0; z <= 100; z++)
            {
                t3++;
                if (x + y + z == 100 && z % 3 == 0 && 5 * x + 3 * y + z / 3 == 100)
                {
                    s3++;
                }
            }
        }
    }
    printf("两层循环：试了 %ld 次，找到 %d 组\n", t2, s2);
    printf("三层循环：试了 %ld 次，找到 %d 组\n", t3, s3);
    return 0;
}
