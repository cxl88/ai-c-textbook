/* 程序名：bad_nocol.c
   功能：错误示范：二维数组省略了列数（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    int d[2][] = {{1, 2, 3}, {4, 5, 6}};

    printf("%d\n", d[0][0]);
    return 0;
}
