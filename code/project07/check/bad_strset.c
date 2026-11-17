/* 程序名：bad_strset.c
   功能：错误示范：用赋值号给字符数组赋一个字符串（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    char s[10];

    s = "正常";
    printf("%s\n", s);
    return 0;
}
