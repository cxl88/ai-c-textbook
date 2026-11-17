/* 程序名：state_text.c
   功能：录入 8 路测点的电压和状态文本，对照输出（任务四 第一步） */
#include <stdio.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    char state[8][10];                 // 8 条状态文本，最多 4 个汉字
    int i;

    for (i = 0; i < 8; i++)            // 录入
    {
        printf("请输入V%d的电压和状态：", i + 1);
        scanf("%f%s", &v[i], state[i]);
    }
    printf("测点   电压（V）  状态\n");
    for (i = 0; i < 8; i++)            // 对照输出
    {
        printf("  V%d%12.2f  %s\n", i + 1, v[i], state[i]);
    }
    return 0;
}
