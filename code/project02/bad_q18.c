/* 程序名：bad_q18.c
   功能：求三次温度的平均值，并输出温度单位（有 3 处错误） */
#include <stdio.h>

int main(void)
{
    int t1 = 24, t2 = 25, t3 = 27;      // 三次温度（℃）
    double avg;                         // 平均温度
    char unit = "C";                    // 温度单位

    avg = (t1 + t2 + t3) / 3;
    printf("平均温度：%d °%c\n", avg, unit);
    return 0;
}
