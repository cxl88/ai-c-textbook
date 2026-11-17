/* 程序名：bad_nolen.c
   功能：错误示范：既不写长度，也不赋初值（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    int a[];

    return 0;
}
