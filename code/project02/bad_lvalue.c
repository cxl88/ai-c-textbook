#include <stdio.h>

int main(void)
{
    int a = 5;
    5++;                        // 错误：自增运算只能用于变量
    a + 1 = 7;                  // 错误：赋值号左边必须是变量
    printf("%d\n", a);
    return 0;
}
