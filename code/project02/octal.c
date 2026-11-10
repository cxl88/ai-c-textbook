#include <stdio.h>

int main(void)
{
    printf("%d\n", 203);    // 十进制整数 203
    printf("%d\n", 0203);   // 以 0 开头：八进制整数
    printf("%d\n", 0x1F);   // 以 0x 开头：十六进制整数
    return 0;
}
