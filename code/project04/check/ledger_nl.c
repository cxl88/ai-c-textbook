/* 程序名：ledger.c
   功能：录入 5 个电阻的阻值，输出电阻实训台账 */
#include <stdio.h>

int main(void)
{
    float r1, r2, r3, r4, r5;          // 5 个电阻的阻值（kΩ）

    /* 第一步：输入阻值 */
    printf("请输入 5 个电阻的阻值（kΩ，用空格隔开）：\n");
    scanf("%f%f%f%f%f", &r1, &r2, &r3, &r4, &r5);

    /* 第二步：处理（本任务不需要处理） */

    /* 第三步：输出台账 */
    printf("------ 电阻实训台账 ------\n");
    printf("序号        阻值\n");
    printf("%4d%12.2f\n", 1, r1);
    printf("%4d%12.2f\n", 2, r2);
    printf("%4d%12.2f\n", 3, r3);
    printf("%4d%12.2f\n", 4, r4);
    printf("%4d%12.2f\n", 5, r5);
    printf("--------------------------\n");
    printf("阻值单位：kΩ    登记人：林小禾\n");
    return 0;
}
