/* 程序名：usage.c
   功能：统计 0203 实训室的座位利用率和教师计算机的功率 */
#include <stdio.h>

int main(void)
{
    int seats, people;          // 总座位数、当前在室人数
    double rate;                // 座位利用率（%）
    double volt, amp, power;    // 电压（V）、电流（A）、功率（W）

    seats = 48;                 // 输入：本项目用赋值代替键盘输入
    people = 36;
    volt = 218.6;
    amp = 1.25;

    rate = (double)people / seats * 100;   // 处理 1：座位利用率
    power = volt * amp;                    // 处理 2：功率 P = U × I

    printf("====== 0203 实训室利用情况 ======\n");
    printf("总座位数：%d    在室人数：%d\n", seats, people);
    printf("座位利用率：%.1f%%\n", rate);
    printf("工作电压：%.1f V   工作电流：%.2f A\n", volt, amp);
    printf("计算机功率：%.2f W\n", power);
    return 0;
}
