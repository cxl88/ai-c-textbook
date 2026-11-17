/* 程序名：ai_b.c
   功能：AI 给出的办法②：排序前复制一份，排序后再查原来的位置 */
#include <stdio.h>

int main(void)
{
    float v[8], old[8], t;             // 电压、排序前的副本、临时变量
    int i, j, k;

    printf("请输入V1～V8的电压：");
    for (i = 0; i < 8; i++)
    {
        scanf("%f", &v[i]);
        old[i] = v[i];
    }
    for (i = 0; i < 7; i++)
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
        for (k = 0; k < 8; k++)        // 在副本中查找这个电压
        {
            if (old[k] == v[i])
            {
                break;
            }
        }
        printf("V%d  %5.2f\n", k + 1, v[i]);
    }
    return 0;
}
