/* 程序名：bill.c
   功能：计算实训室计算机一天的用电量和电费 */
#include <stdio.h>

int main(void)
{
    int pcs = 30;               // 计算机台数
    double power = 273.25;      // 每台计算机的功率（W）
    int hours = 8;              // 每天开机时间（小时）
    double price = 0.62;        // 电价（元/千瓦时）
    double kwh, fee;            // 用电量（千瓦时）、电费（元）

    kwh = pcs * power * hours / 1000;      // W × h ÷ 1000 = kW·h
    fee = kwh * price;
    printf("每天用电量：%.2f 千瓦时\n", kwh);
    printf("每天电费：%.2f 元\n", fee);
    return 0;
}
