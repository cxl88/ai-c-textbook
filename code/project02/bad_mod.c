#include <stdio.h>

int main(void)
{
    double t = 24.5;
    printf("%d\n", t % 2);      // 错误：% 的两边必须是整数
    return 0;
}
