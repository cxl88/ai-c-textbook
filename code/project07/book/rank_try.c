/* 程序名：rank_try.c
   功能：8 路电压从低到高排序后输出（林小禾的第一次尝试） */
#include <stdio.h>

int main(void)
{
    float v[8], t;                     // 8 路测点电压（V）、临时变量
    int i, j;

    printf("请输入V1～V8的电压：");
    for (i = 0; i < 8; i++)
    {
        scanf("%f", &v[i]);
    }
    for (i = 0; i < 7; i++)            // 冒泡排序，与 bubble.c 相同
    {
        for (j = 0; j < 7 - i; j++)
        {
            if (v[j] > v[j + 1])
            {
                t = v[j];
                v[j] = v[j + 1];
                v[j + 1] = t;
            }
        }
    }
    printf("从低到高：\n");
    for (i = 0; i < 8; i++)
    {
        printf("V%d  %5.2f\n", i + 1, v[i]);
    }
    return 0;
}
