#include <stdio.h>

int main(void)
{
    float balance, cost;

    balance = 100;                       // 当前卡内余额（元）
    printf("本次消费：");
    scanf("%f", &cost);                  // ① 输入消费金额
    balance = balance - cost;            // ② 计算新余额
    printf("余额：%.2f 元\n", balance);  // ③ 输出余额
    return 0;
}
