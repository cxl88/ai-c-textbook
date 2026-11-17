/* 程序名：cp_more.c
   功能：“离开 AI 再做”参考答案：从高到低排序，编号、状态一起交换 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    float v[8], t;                     // 电压、交换电压用
    int no[8], k;                      // 编号、交换编号用
    char state[8][10], ts[10];         // 状态文本、交换文本用
    int i, j;

    for (i = 0; i < 8; i++)
    {
        printf("请输入V%d的电压和状态：", i + 1);
        scanf("%f%s", &v[i], state[i]);
        no[i] = i + 1;
    }
    for (i = 0; i < 7; i++)
    {
        for (j = 0; j < 7 - i; j++)
        {
            if (v[j] < v[j + 1])       // 前小后大，就交换
            {
                t = v[j];
                v[j] = v[j + 1];
                v[j + 1] = t;
                k = no[j];
                no[j] = no[j + 1];
                no[j + 1] = k;
                strcpy(ts, state[j]);  // 字符串要用 strcpy 交换
                strcpy(state[j], state[j + 1]);
                strcpy(state[j + 1], ts);
            }
        }
    }
    for (i = 0; i < 8; i++)
    {
        printf("  V%d%8.2f  %s\n", no[i], v[i], state[i]);
    }
    return 0;
}
