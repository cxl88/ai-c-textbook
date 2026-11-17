/* 程序名：bubble.c
   功能：用冒泡法把 8 路测点电压从低到高排序 */
#include <stdio.h>

int main(void)
{
    float v[8] = {4.02, 3.98, 12.00, 4.05, 3.42, 0.00, 3.96, 4.01};
    float t;                           // 交换时临时存放
    int i, j;

    for (i = 0; i < 7; i++)            // 8 个数，共比较 7 轮
    {
        for (j = 0; j < 7 - i; j++)    // 第 i+1 轮比较 7-i 次
        {
            if (v[j] > v[j + 1])       // 前大后小，就交换
            {
                t = v[j];
                v[j] = v[j + 1];
                v[j + 1] = t;
            }
        }
    }
    printf("从低到高：");
    for (i = 0; i < 8; i++)
    {
        printf("%.2f ", v[i]);
    }
    printf("\n");
    return 0;
}
