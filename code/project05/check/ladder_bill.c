/* 程序名：ladder_bill.c
   功能：实训巩固挑战题参考答案：居民阶梯电价（数据为教学模拟） */
#include <stdio.h>

int main(void)
{
    int kwh;                           // 月用电量（度）
    double fee;                        // 电费（元）

    printf("月用电量（度）：");
    scanf("%d", &kwh);
    if (kwh <= 200)
    {
        fee = kwh * 0.56;
    }
    else if (kwh <= 400)
    {
        fee = 200 * 0.56 + (kwh - 200) * 0.61;
    }
    else
    {
        fee = 200 * 0.56 + 200 * 0.61 + (kwh - 400) * 0.86;
    }
    printf("应缴电费：%.2f 元\n", fee);
    return 0;
}
