/* 程序名：cp_io.c
   功能：核对课堂练习：字符串的输出 */
#include <stdio.h>

int main(void)
{
    char s[] = "abc";

    printf("%s|%c|%d\n", s, s[1], s[3]);
    puts(s);
    puts("OK");
    return 0;
}
