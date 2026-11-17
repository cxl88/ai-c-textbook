/* 程序名：bad_hz.c
   功能：错误示范：把一个汉字存进 char 型变量（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    char c = '开';

    printf("%c\n", c);
    return 0;
}
