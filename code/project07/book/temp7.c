/* 程序名：temp7.c
   功能：一周最高气温：哪天最热，一周温差多大（任务一 技能训练 3） */
#include <stdio.h>

int main(void)
{
    int t[7];                          // 7 天的最高气温（℃）
    int i, k = 0, min;                 // 下标、最热一天的下标、最低值

    printf("请输入7天的最高气温（用空格隔开）：");
    for (i = 0; i < 7; i++)
    {
        scanf("%d", &t[i]);
    }
    min = t[0];
    for (i = 1; i < 7; i++)
    {
        if (t[i] > t[k])
        {
            k = i;
        }
        if (t[i] < min)
        {
            min = t[i];
        }
    }
    printf("最热的是第%d天：%d℃\n", k + 1, t[k]);
    printf("一周温差：%d℃\n", t[k] - min);
    return 0;
}
