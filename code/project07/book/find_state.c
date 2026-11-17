/* 程序名：find_state.c
   功能：录入 8 路测点后，按状态文本查找支路（任务四 技能训练 2） */
#include <stdio.h>
#include <string.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    char state[8][10];                 // 8 条状态文本
    char key[10];                      // 要查找的状态
    int i, found = 0;                  // 下标、找到的支路数

    for (i = 0; i < 8; i++)
    {
        printf("请输入V%d的电压和状态：", i + 1);
        scanf("%f%s", &v[i], state[i]);
    }
    printf("请输入要查找的状态：");
    scanf("%s", key);
    for (i = 0; i < 8; i++)
    {
        if (strcmp(state[i], key) == 0)
        {
            printf("  V%d%8.2f V\n", i + 1, v[i]);
            found++;
        }
    }
    if (found == 0)
    {
        printf("没有处于这种状态的支路\n");
    }
    return 0;
}
