/* 程序名：elec.c
   功能：输入上月和本月的电表读数，计算本月用电量和应缴电费（实训巩固第 14 题参考答案） */
#include <stdio.h>

int main(void)
{
    int last, now, used;                 // 上月读数、本月读数、用电量（度）
    float price = 0.56, fee;             // 电价（元/度）、电费（元）

    printf("请输入上月和本月的电表读数（用空格隔开）：");
    scanf("%d%d", &last, &now);
    used = now - last;
    fee = used * price;
    printf("本月用电 %d 度，应缴电费 %.2f 元\n", used, fee);
    return 0;
}
