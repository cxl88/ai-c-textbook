/* 程序名：series.c
   功能：输入两个电阻的阻值，求串联和并联后的总电阻 */
#include <stdio.h>

int main(void)
{
    float r1, r2;                      // 两个电阻的阻值（kΩ）
    float rs, rp;                      // 串联、并联后的总电阻（kΩ）

    printf("请输入两个电阻的阻值（kΩ）：");
    scanf("%f%f", &r1, &r2);              // 输入
    rs = r1 + r2;                         // 处理：串联
    rp = r1 * r2 / (r1 + r2);             // 处理：并联
    printf("串联总电阻：%.2f kΩ\n", rs);  // 输出
    printf("并联总电阻：%.2f kΩ\n", rp);
    return 0;
}
