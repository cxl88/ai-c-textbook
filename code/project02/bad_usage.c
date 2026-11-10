/* 程序名：bad_usage.c（某同学的初稿）
   功能：统计座位利用率和计算机功率 */
#include <stdio.h>

int main(void)
{
    int seats = 48, people = 36;        // 总座位数、在室人数
    int rate;                           // 座位利用率（%）
    double volt = 218.6, amp = 1.25;    // 工作电压（V）、工作电流（A）
    double power;                       // 功率（W）

    rate = people / seats * 100;
    power = volt amp;
    printf("座位利用率：%d%\n", rate);
    printf("计算机功率：%d W\n", power);
    return 0;
}
