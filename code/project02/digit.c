#include <stdio.h>

int main(void)
{
    char ch = '7';              // 数字字符 7
    int n = ch - '0';           // 数字字符相减：实际上是 ASCII 码相减
    printf("字符 %c 的 ASCII 码：%d\n", ch, ch);
    printf("得到的整数：%d\n", n);
    printf("整数加 1：%d\n", n + 1);
    return 0;
}
