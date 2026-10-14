#include <stdio.h>

int main(void)
{
    _Bool power = 1;                    // 布尔型变量：1 表示开机
    printf("开机状态：%d\n", power);
    power = 0;                          // 0 表示关机
    printf("开机状态：%d\n", power);
    power = 5;                          // 非 0 的值存入后都变成 1
    printf("开机状态：%d\n", power);
    return 0;
}
