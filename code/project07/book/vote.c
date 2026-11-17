/* 程序名：vote.c
   功能：统计 10 张选票中 A、B、C 三位候选人的得票数 */
#include <stdio.h>

int main(void)
{
    char v[10];                        // 10 张选票
    int cnt[3] = {0};                  // A、B、C 的票数
    int i, bad = 0;                    // 下标、废票数

    printf("请输入10张选票：");
    for (i = 0; i < 10; i++)
    {
        scanf(" %c", &v[i]);
    }
    for (i = 0; i < 10; i++)
    {
        if (v[i] >= 'A' && v[i] <= 'C')
        {
            cnt[v[i] - 'A']++;         // 'A' 计入 cnt[0]，依此类推
        }
        else
        {
            bad++;
        }
    }
    printf("A：%d票  B：%d票  C：%d票\n", cnt[0], cnt[1], cnt[2]);
    printf("废票：%d张\n", bad);
    return 0;
}
