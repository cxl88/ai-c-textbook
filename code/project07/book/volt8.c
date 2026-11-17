/* 程序名：volt8.c
   功能：录入并显示 8 路分压测点的电压（任务一） */
#include <stdio.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    int i;                             // 下标：0～7 对应 V1～V8

    for (i = 0; i < 8; i++)            // 录入
    {
        printf("请输入V%d的电压（V）：", i + 1);
        scanf("%f", &v[i]);
    }
    printf("测点   电压（V）\n");
    for (i = 0; i < 8; i++)            // 显示
    {
        printf("  V%d%12.2f\n", i + 1, v[i]);
    }
    return 0;
}
