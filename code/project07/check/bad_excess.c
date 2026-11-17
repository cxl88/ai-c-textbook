/* 程序名：bad_excess.c
   功能：错误示范：初值个数多于数组长度（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    int d[3] = {1, 2, 3, 4};

    printf("%d\n", d[0]);
    return 0;
}
