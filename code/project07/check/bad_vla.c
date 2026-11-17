/* 程序名：bad_vla.c
   功能：错误示范：用变量定义数组的长度（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    int n = 8;
    float v[n];

    v[0] = 4.02;
    printf("%.2f\n", v[0]);
    return 0;
}
