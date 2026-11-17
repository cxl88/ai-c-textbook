/* 程序名：volt83.c
   功能：录入 3 轮电压后，按测点显示（任务二 技能训练 2） */
#include <stdio.h>

int main(void)
{
    float v[3][8];                     // 3 轮 × 8 路测点电压（V）
    int i, j;                          // 行下标、列下标

    for (i = 0; i < 3; i++)
    {
        printf("第%d轮V1～V8：", i + 1);
        for (j = 0; j < 8; j++)
        {
            scanf("%f", &v[i][j]);
        }
    }
    printf("测点  第1轮  第2轮  第3轮\n");
    for (j = 0; j < 8; j++)            // 外层：逐个测点
    {
        printf("  V%d", j + 1);
        for (i = 0; i < 3; i++)        // 内层：逐轮
        {
            printf("%7.2f", v[i][j]);
        }
        printf("\n");
    }
    return 0;
}
