#include <stdio.h>

int main(void)
{
    char code = 'g';                              // 告警字母 g
    printf("%c 的 ASCII 码是 %d\n", code, code);
    printf("%c 的 ASCII 码是 %d\n", 'G', 'G');
    printf("两者相差：%d\n", 'g' - 'G');
    printf("字符 A 的 ASCII 码是 %d\n", 'A');
    printf("字符 0 的 ASCII 码是 %d\n", '0');
    return 0;
}
