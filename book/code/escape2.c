#include <stdio.h>

int main(void)
{
    printf("单引号\'  双引号\"  反斜杠\\\n");
    printf("A\tB\tC\n");                      // \t：跳到下一个制表位
    printf("\101 \x42 \103\n");               // 八进制 101、十六进制 42、八进制 103
    return 0;
}
