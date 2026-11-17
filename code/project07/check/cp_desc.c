/* 程序名：cp_desc.c
   功能：课堂练习参考答案：从高到低排序 */
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
            if (v[j] < v[j + 1])       // 前小后大，就交换
            {
                t = v[j];
                v[j] = v[j + 1];
                v[j + 1] = t;
            }
        }
    }
    printf("从高到低：");
    for (i = 0; i < 8; i++)
    {
        printf("%.2f ", v[i]);
    }
    printf("\n");
    return 0;
}
