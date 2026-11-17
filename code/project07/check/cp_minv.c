/* 程序名：cp_minv.c
   功能：课堂练习参考答案：找出电压最低的测点 */
#include <stdio.h>

int main(void)
{
    float v[8] = {4.02, 3.98, 12.00, 4.05, 3.42, 0.00, 3.96, 4.01};
    float min;                         // 最小值
    int i, k;                          // 下标、最大值的下标

    min = v[0];                        // 先假设第 1 路最小
    k = 0;
    for (i = 1; i < 8; i++)
    {
        if (v[i] < min)                // 发现更小的，记下它和它的下标
        {
            min = v[i];
            k = i;
        }
    }
    printf("电压最低的是V%d：%.2f V\n", k + 1, min);
    return 0;
}
