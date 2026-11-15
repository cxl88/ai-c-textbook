/* 程序名：avg_valid.c
   功能：输入 6 次电压测量值，跳过无效的负数，求有效值的平均值（任务三 技能训练 3） */
#include <stdio.h>

int main(void)
{
    float v, sum = 0;                  // 测量值、有效值之和
    int i, n = 0;                      // n：有效值的个数

    printf("请输入 6 次电压测量值（V）：");
    for (i = 1; i <= 6; i++)
    {
        scanf("%f", &v);
        if (v < 0)                     // 负数：测量失误，跳过
        {
            printf("第%d次测量值 %.1f 无效，跳过\n", i, v);
            continue;
        }
        sum = sum + v;
        n++;
    }
    if (n > 0)
    {
        printf("有效测量 %d 次，平均电压 %.2f V\n", n, sum / n);
    }
    else
    {
        printf("没有有效的测量值\n");
    }
    return 0;
}
