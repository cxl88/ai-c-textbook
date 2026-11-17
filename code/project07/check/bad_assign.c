/* 程序名：bad_assign.c
   功能：错误示范：给数组整体赋值（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    int a[3] = {1, 2, 3}, b[3], c[3];

    b = a;
    c = {1, 2, 3};
    return 0;
}
