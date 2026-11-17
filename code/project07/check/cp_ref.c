/* 程序名：cp_ref.c
   功能：核对课堂练习：一维数组的引用 */
#include <stdio.h>

int main(void)
{
    int a[5] = {1, 2, 3, 4, 5}, b[5] = {0};
    int i;

    for (i = 4; i >= 0; i--)
    {
        printf("%d ", a[i]);
    }
    printf("\n");
    for (i = 0; i < 5; i++)
    {
        b[i] = i * i;
    }
    printf("b[3]=%d\n", b[3]);
    return 0;
}
