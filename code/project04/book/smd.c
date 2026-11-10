/* 程序名：smd.c
   功能：输入贴片电阻上的 3 位数字代码，求阻值 */
#include <stdio.h>
#include <math.h>

int main(void)
{
    char c1, c2, c3;                   // 3 位代码，如 4、7、2
    double r;                          // 阻值（Ω）

    printf("请输入贴片电阻上的 3 位代码：");
    c1 = getchar();
    c2 = getchar();
    c3 = getchar();
    r = ((c1 - '0') * 10 + (c2 - '0')) * pow(10, c3 - '0');
    printf("阻值：%.0f Ω，即 %.2f kΩ\n", r, r / 1000);
    return 0;
}
