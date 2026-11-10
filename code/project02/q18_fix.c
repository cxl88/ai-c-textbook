/* 程序名：q18_fix.c
   功能：求三次温度的平均值，并输出温度单位（第 18 题改正后） */
#include <stdio.h>

int main(void)
{
    int t1 = 24, t2 = 25, t3 = 27;      // 三次温度（℃）
    double avg;                         // 平均温度
    char unit = 'C';                    // 温度单位

    avg = (t1 + t2 + t3) / 3.0;
    printf("平均温度：%.1f °%c\n", avg, unit);
    return 0;
}
