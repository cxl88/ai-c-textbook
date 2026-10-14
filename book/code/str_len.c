#include <stdio.h>
#include <string.h>

int main(void)
{
    char c = 'g';
    printf("字符 c 占 %d 字节\n", (int)sizeof(c));
    printf("字符串 \"g\" 占 %d 字节，", (int)sizeof("g"));
    printf("长度为 %d\n", (int)strlen("g"));
    printf("字符串 \"203\" 的长度为 %d\n", (int)strlen("203"));
    return 0;
}
