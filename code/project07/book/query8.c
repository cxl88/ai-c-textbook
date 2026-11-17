/* 程序名：query8.c
   功能：录入 8 路测点电压，再按编号查询（任务一 技能训练 2） */
#include <stdio.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    int i, k;                          // 下标、要查询的测点编号

    for (i = 0; i < 8; i++)
    {
        printf("请输入V%d的电压（V）：", i + 1);
        scanf("%f", &v[i]);
    }
    printf("请输入要查询的测点编号（1～8）：");
    scanf("%d", &k);
    if (k >= 1 && k <= 8)              // 编号有效，才能用作下标
    {
        printf("V%d的电压：%.2f V\n", k, v[k - 1]);
    }
    else
    {
        printf("没有这个测点！\n");
    }
    return 0;
}
