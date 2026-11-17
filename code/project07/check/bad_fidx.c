/* 程序名：bad_fidx.c
   功能：错误示范：下标不是整数（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    float v[8] = {0};

    printf("%.2f\n", v[1.5]);
    return 0;
}
