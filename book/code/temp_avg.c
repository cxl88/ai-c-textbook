#include <stdio.h>

int main(void)
{
    double t1 = 24.5, t2 = 25.1, t3 = 23.9;     // 上午三次测得的温度（℃）
    double avg;                                 // 平均温度

    avg = (t1 + t2 + t3) / 3;
    printf("三次温度：%.1f  %.1f  %.1f\n", t1, t2, t3);
    printf("平均温度：%.1f ℃\n", avg);
    return 0;
}
