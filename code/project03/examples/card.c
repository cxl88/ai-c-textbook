/* 程序名：card.c
   功能：校园卡消费后计算余额（顺序结构） */
#include <stdio.h>

int main(void)
{
    float balance, cost;

    printf("校园卡余额：");
    scanf("%f", &balance);             // ① 读入余额
    printf("本次消费：");
    scanf("%f", &cost);                // ② 读入消费金额
    balance = balance - cost;          // ③ 计算新余额
    printf("消费成功，余额：%.2f 元\n", balance);   // ④ 输出
    return 0;
}
