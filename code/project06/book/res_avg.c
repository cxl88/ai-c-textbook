/* 程序名：res_avg.c
   功能：依次输入电阻的阻值，输入 0 结束，求测量个数和平均阻值（任务一 技能训练 3） */
#include <stdio.h>

int main(void)
{
    float r, sum = 0;                  // 阻值、阻值之和
    int n = 0;                         // 测量的个数

    printf("第1个电阻的阻值（Ω，输入0结束）：");
    scanf("%f", &r);
    while (r != 0)                     // 不是 0，就是一个有效的阻值
    {
        n++;
        sum = sum + r;
        printf("第%d个电阻的阻值（Ω，输入0结束）：", n + 1);
        scanf("%f", &r);
    }
    if (n == 0)
    {
        printf("没有测量数据\n");
    }
    else
    {
        printf("共测量 %d 个电阻，平均阻值 %.2f Ω\n", n, sum / n);
    }
    return 0;
}
