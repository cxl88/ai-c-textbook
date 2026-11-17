/* 程序名：abn8.c
   功能：找出电压不在 3.8～4.2 V 之间的测点（任务一 技能训练 1） */
#include <stdio.h>

int main(void)
{
    float v[8] = {4.02, 3.98, 12.00, 4.05, 3.42, 0.00, 3.96, 4.01};
    int i, count = 0;                  // 下标、异常的测点数

    printf("电压异常的测点：");
    for (i = 0; i < 8; i++)
    {
        if (v[i] < 3.8 || v[i] > 4.2)
        {
            printf("V%d（%.2f V） ", i + 1, v[i]);
            count++;
        }
    }
    printf("\n共%d路\n", count);
    return 0;
}
