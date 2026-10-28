#include <stdio.h>

int main(void)
{
    int i;
    float r, sum;

    sum = 0;
    i = 1;
    while (i <= 5)
    {
        printf("第%d次测量值（Ω）：", i);
        scanf("%f", &r);
        sum = sum + r;
    }
    printf("平均阻值：%.2f Ω\n", sum / 5);
    return 0;
}
