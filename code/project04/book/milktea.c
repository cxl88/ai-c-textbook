/* 程序名：milktea.c
   功能：输入杯数、杯型和单价，输出奶茶点单小票 */
#include <stdio.h>

int main(void)
{
    int cups;                          // 杯数
    char size;                         // 杯型：M 中杯，L 大杯
    float price, total;                // 单价、总价（元）

    printf("杯数：");
    scanf("%d", &cups);
    getchar();                         // 读走杯数后面的回车符
    printf("杯型（M 中杯，L 大杯）：");
    size = getchar();
    printf("单价（元）：");
    scanf("%f", &price);
    total = cups * price;
    printf("====== 点单小票 ======\n");
    printf("杯型：");
    putchar(size);
    putchar('\n');
    printf("杯数：%d 杯\n", cups);
    printf("单价：%.2f 元\n", price);
    printf("总价：%.2f 元\n", total);
    printf("======================\n");
    return 0;
}
