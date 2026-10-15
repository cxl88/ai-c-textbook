/* 程序名：ohm.c
   功能：已知电压和电阻，用欧姆定律求电流 */
#include <stdio.h>

int main(void)
{
    float u, r, i;                     // 电压 V、电阻 kΩ、电流 mA

    printf("请输入电压（V）和电阻（kΩ）：");
    scanf("%f%f", &u, &r);               // ① ②：输入电压和电阻
    i = u / r;                           // 单位：V / kΩ = mA
    printf("电流 I = %.2f mA\n", i);     // ③：保留 2 位小数输出
    return 0;
}
