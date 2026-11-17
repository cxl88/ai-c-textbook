/* 程序名：cp_cinit.c
   功能：核对课堂练习：字符数组的初始化 */
#include <stdio.h>

int main(void)
{
    char c[5] = {'a', 'b'};
    char d[] = {'O', 'K'};

    printf("c[2]=%d，d有%d个元素\n", c[2], (int)sizeof(d));
    return 0;
}
