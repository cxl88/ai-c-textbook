/* 程序名：q13.c
   功能：输入上月和本月电表读数，计算用电量和电费 */
#include <stdio.h>

#define PRICE 0.56                     // 电价：元/度

int main(void)
{
    int last, now, used;               // 上月读数、本月读数、用电量（度）
    double fee;                        // 电费（元）

    printf("请输入上月和本月的电表读数：");
    scanf("%d%d", &last, &now);
    used = now - last;
    fee = used * PRICE;
    printf("本月用电：%d 度\n", used);
    printf("应缴电费：%.2f 元\n", fee);
    return 0;
}
