/* 程序名：cp_caesar.c
   功能：核对课堂练习：Wuxi 加密后是什么 */
#include <stdio.h>

int main(void)
{
    char s[4] = {'W', 'u', 'x', 'i'};
    int i;

    for (i = 0; i < 4; i++)
    {
        s[i] = s[i] + 4;               // 向后移 4 位
        if (s[i] > 'z' || (s[i] > 'Z' && s[i] < 'a'))
        {
            s[i] = s[i] - 26;          // 超出了字母表，绕回开头
        }
    }
    printf("加密后：");
    for (i = 0; i < 4; i++)
    {
        printf("%c", s[i]);
    }
    printf("\n");
    return 0;
}
