#include <stdio.h>
#include <string.h>

int main(void)
{
    char c = 'g';               // 字符型变量 c，存放字符 g
    printf("变量 c 占 %d 字节\n", (int)sizeof(c));
    printf("字符串 \"g\" 占 %d 字节，", (int)sizeof("g"));
    printf("长度为 %d\n", (int)strlen("g"));
    printf("字符串 \"203\" 占 %d 字节，", (int)sizeof("203"));
    printf("长度为 %d\n", (int)strlen("203"));
    return 0;
}
