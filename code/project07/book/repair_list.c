/* 程序名：repair_list.c
   功能：对照输出电压和状态，列出需要检修的支路（任务四 第二步） */
#include <stdio.h>
#include <string.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    char state[8][10];                 // 8 条状态文本，最多 4 个汉字
    int i, count = 0;                  // 下标、需要检修的支路数

    for (i = 0; i < 8; i++)
    {
        printf("请输入V%d的电压和状态：", i + 1);
        scanf("%f%s", &v[i], state[i]);
    }
    printf("测点   电压（V）  状态\n");
    for (i = 0; i < 8; i++)
    {
        printf("  V%d%12.2f  %s\n", i + 1, v[i], state[i]);
    }
    printf("需要检修的支路：");
    for (i = 0; i < 8; i++)
    {
        if (strcmp(state[i], "支路正常") != 0)  // 状态不是“支路正常”
        {
            printf("V%d（%s） ", i + 1, state[i]);
            count++;
        }
    }
    printf("\n共%d路\n", count);
    return 0;
}
