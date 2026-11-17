/* 程序名：maxv.c
   功能：找出 8 路测点电压中的最大值，以及它是哪一路 */
#include <stdio.h>

int main(void)
{
    float v[8] = {4.02, 3.98, 12.00, 4.05, 3.42, 0.00, 3.96, 4.01};
    float max;                         // 最大值
    int i, k;                          // 下标、最大值的下标

    max = v[0];                        // 先假设第 1 路最大
    k = 0;
    for (i = 1; i < 8; i++)
    {
        if (v[i] > max)                // 发现更大的，记下它和它的下标
        {
            max = v[i];
            k = i;
        }
    }
    printf("电压最高的是V%d：%.2f V\n", k + 1, max);
    return 0;
}
