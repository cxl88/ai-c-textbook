/* 程序名：cp_init.c
   功能：核对课堂练习：一维数组初始化 */
#include <stdio.h>

int main(void)
{
    int a[5] = {2, 4};
    int b[] = {1, 3, 5, 7};

    printf("a[1]=%d a[3]=%d\n", a[1], a[3]);
    printf("b的长度：%d\n", (int)(sizeof(b) / sizeof(b[0])));
    return 0;
}
