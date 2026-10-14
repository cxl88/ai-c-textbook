/* 技能训练 2（任务二）参考：按阻值分到三个盒子（选择中再套选择） */
#include <stdio.h>

int main(void)
{
    int i;
    float r;

    i = 1;
    while (i <= 5)
    {
        printf("第%d个电阻的阻值（Ω）：", i);
        scanf("%f", &r);
        if (r > 105)
        {
            printf("  放入偏大盒\n");
        }
        else
        {
            if (r < 95)
            {
                printf("  放入偏小盒\n");
            }
            else
            {
                printf("  放入合格盒\n");
            }
        }
        i = i + 1;
    }
    return 0;
}
