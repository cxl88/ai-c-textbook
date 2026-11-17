/* 程序名：cp_digit.c
   功能：核对课堂练习：统计字符串中数字的个数 */
#include <stdio.h>

int main(void)
{
    char s[] = "a1b2c3";
    int i, n = 0;

    for (i = 0; s[i] != '\0'; i++)
    {
        if (s[i] >= '0' && s[i] <= '9')
        {
            n++;
        }
    }
    printf("%d\n", n);
    return 0;
}
