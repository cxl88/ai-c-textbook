/* 程序名：avg_temp.c
   功能：求上午三次温度的平均值 */
#include <stdio.h>

int main(void)
{
    float t1 = 24.5, t2 = 25.1, t3 = 23.9;   // 三次测得的温度（℃）
    float avg;                               // 平均温度

    avg = (t1 + t2 + t3) / 3;
    printf("三次温度：%.1f  %.1f  %.1f\n", t1, t2, t3);
    printf("平均温度：%.1f ℃\n", avg);
    return 0;
}
