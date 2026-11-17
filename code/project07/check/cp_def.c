/* 程序名：cp_def.c
   功能：核对课堂练习：正确的数组定义 */
#include <stdio.h>
#define N 8

int main(void)
{
    float v[8];
    float w[N];
    int a[2 + 3];

    printf("%d ", (int)(sizeof(v) / sizeof(v[0])));
    printf("%d ", (int)(sizeof(w) / sizeof(w[0])));
    printf("%d\n", (int)(sizeof(a) / sizeof(a[0])));
    return 0;
}
