/* 程序名：bad_comma.c
   功能：for 语句易错点①：圆括号中用逗号代替分号（只编译） */
#include <stdio.h>

int main(void)
{
    int i, sum = 0;

    for (i = 1, i <= 100, i++)
    {
        sum = sum + i;
    }
    printf("1+2+…+100 = %d\n", sum);
    return 0;
}
