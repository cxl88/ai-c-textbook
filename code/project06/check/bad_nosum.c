/* 程序名：bad_nosum.c
   功能：while 语句易错点③：sum 没有赋初值（只编译） */
#include <stdio.h>

int main(void)
{
    int i, sum;

    i = 1;
    while (i <= 100)
    {
        sum = sum + i;
        i++;
    }
    printf("1+2+…+100 = %d\n", sum);
    return 0;
}
