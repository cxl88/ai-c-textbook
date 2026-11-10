/* 程序名：volt_dev.c
   功能：在 usage.c 的基础上增加电压偏差率 */
#include <stdio.h>
#define RATED 220               // 额定电压（V）

int main(void)
{
    int seats, people;          // 总座位数、当前在室人数
    double rate;                // 座位利用率（%）
    double volt, amp, power;    // 电压（V）、电流（A）、功率（W）
    double dev;                 // 新增：电压偏差率（%）

    seats = 48;
    people = 36;
    volt = 218.6;
    amp = 1.25;

    rate = (double)people / seats * 100;
    power = volt * amp;
    dev = (volt - RATED) / RATED * 100;    // 新增：电压偏差率

    printf("====== 0203 实训室利用情况 ======\n");
    printf("总座位数：%d    在室人数：%d\n", seats, people);
    printf("座位利用率：%.1f%%\n", rate);
    printf("工作电压：%.1f V   工作电流：%.2f A\n", volt, amp);
    printf("计算机功率：%.2f W\n", power);
    printf("电压偏差率：%.2f%%\n", dev);
    return 0;
}
