/* 程序名：res_sum.c
   功能：输入 5 个电阻的阻值，求串联后的总电阻（任务二 技能训练 1） */
#include <stdio.h>

int main(void)
{
    float r, total = 0;                // 阻值、总电阻
    int i;

    for (i = 1; i <= 5; i++)
    {
        printf("第%d个电阻的阻值（kΩ）：", i);
        scanf("%f", &r);
        total = total + r;             // 串联：总电阻等于各电阻之和
    }
    printf("串联后的总电阻：%.2f kΩ\n", total);
    return 0;
}
