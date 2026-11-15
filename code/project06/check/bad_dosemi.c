/* 程序名：bad_dosemi.c
   功能：do…while 语句易错点①：末尾漏写分号（只编译） */
#include <stdio.h>

int main(void)
{
    int i = 1, sum = 0;

    do
    {
        sum = sum + i;
        i++;
    } while (i <= 100)
    printf("1+2+…+100 = %d\n", sum);
    return 0;
}
