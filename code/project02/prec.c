#include <stdio.h>

int main(void)
{
    double c = 24.5;            // 摄氏温度（℃）
    double f1, f2, f3;          // 换算成的华氏温度（℉）

    f1 = c * 9 / 5 + 32;        // 从左往右：先算 c * 9
    f2 = 9 / 5 * c + 32;        // 先算 9 / 5：两个整数相除得 1
    f3 = 9.0 / 5 * c + 32;      // 先算 9.0 / 5，得 1.8
    printf("f1 = %.1f\n", f1);
    printf("f2 = %.1f\n", f2);
    printf("f3 = %.1f\n", f3);
    return 0;
}
