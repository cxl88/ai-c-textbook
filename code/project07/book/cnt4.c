/* 程序名：cnt4.c
   功能：统计 4 种状态的支路各有几路（任务三 技能训练 1） */
#include <stdio.h>

int main(void)
{
    char code[8] = {'A', 'A', 'B', 'A', 'D', 'C', 'A', 'A'};
    int cnt[4] = {0};                  // A、B、C、D 各有几路
    int i;

    for (i = 0; i < 8; i++)
    {
        cnt[code[i] - 'A']++;          // 'A' 计入 cnt[0]，依此类推
    }
    printf("支路正常：%d路\n", cnt[0]);
    printf("支路开路：%d路\n", cnt[1]);
    printf("支路短路：%d路\n", cnt[2]);
    printf("接触不良：%d路\n", cnt[3]);
    return 0;
}
