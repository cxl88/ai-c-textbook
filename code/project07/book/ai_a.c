/* 程序名：ai_a.c
   功能：AI 给出的办法①：用数组 no 记录编号，与电压一起交换 */
#include <stdio.h>

int main(void)
{
    float v[8], t;                     // 8 路测点电压（V）、临时变量
    int no[8];                         // 测点编号，与 v 一一对应
    int i, j, k;

    printf("请输入V1～V8的电压：");
    for (i = 0; i < 8; i++)
    {
        scanf("%f", &v[i]);
        no[i] = i + 1;                 // v[i] 是第 i+1 路的电压
    }
    for (i = 0; i < 7; i++)
    {
        for (j = 0; j < 7 - i; j++)
        {
            if (v[j] > v[j + 1])
            {
                t = v[j];              // 交换电压
                v[j] = v[j + 1];
                v[j + 1] = t;
                k = no[j];             // 编号跟着一起交换
                no[j] = no[j + 1];
                no[j + 1] = k;
            }
        }
    }
    printf("从低到高：\n");
    for (i = 0; i < 8; i++)
    {
        printf("V%d  %5.2f\n", no[i], v[i]);
    }
    return 0;
}
