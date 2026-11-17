/* 程序名：cp_init2.c
   功能：核对课堂练习：二维数组的初始化 */
#include <stdio.h>

int main(void)
{
    int a[2][3] = {{1}, {2, 3}};
    int b[][4] = {1, 2, 3, 4, 5};
    int c[2][3] = {1, 2, 3, 4, 5, 6};

    printf("a[0][1]=%d a[1][1]=%d\n", a[0][1], a[1][1]);
    printf("b有%d行，", (int)(sizeof(b) / sizeof(b[0])));
    printf("b[1][0]=%d\n", b[1][0]);
    printf("c[1][0]=%d\n", c[1][0]);
    return 0;
}
