/* 任务二技能训练 2 参考：按阻值分到三个盒子（选择中再套选择），并分别计数 */
#include <stdio.h>

int main(void)
{
    int i, ok, big, small;
    float r;

    ok = 0;
    big = 0;
    small = 0;
    i = 1;
    while (i <= 5)
    {
        printf("第%d个电阻的阻值（Ω）：", i);
        scanf("%f", &r);
        if (r > 105)
        {
            printf("  放入偏大盒\n");
            big = big + 1;
        }
        else
        {
            if (r < 95)
            {
                printf("  放入偏小盒\n");
                small = small + 1;
            }
            else
            {
                printf("  放入合格盒\n");
                ok = ok + 1;
            }
        }
        i = i + 1;
    }
    printf("合格 %d 个，偏大 %d 个，偏小 %d 个\n", ok, big, small);
    return 0;
}
