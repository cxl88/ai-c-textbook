#include <stdio.h>

int main(void)
{
    int i;
    float r, sum;

    sum = 0;
    i = 1;                                // 从第 1 次开始
    while (i <= 5)                        // 还没测满 5 次吗？
    {
        printf("第%d次测量值（Ω）：", i);
        scanf("%f", &r);
        sum = sum + r;                    // 把这次的读数累加起来
        i = i + 1;                        // 次数加 1
    }
    printf("平均阻值：%.2f Ω\n", sum / 5);
    return 0;
}
