#include <stdio.h>

int main(void)
{
    char ch = '7';                      // 数字字符 7
    int n = ch - '0';                   // 减去 '0' 的编码 48，得到整数 7

    printf("字符 %c 的 ASCII 码：%d\n", ch, ch);
    printf("转换得到的整数：%d\n", n);
    printf("整数加 1：%d\n", n + 1);
    return 0;
}
