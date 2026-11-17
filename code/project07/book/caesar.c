/* 程序名：caesar.c
   功能：把每个字母向后移 4 位加密：China 加密为 Glmre */
#include <stdio.h>

int main(void)
{
    char s[5] = {'C', 'h', 'i', 'n', 'a'};
    int i;

    for (i = 0; i < 5; i++)
    {
        s[i] = s[i] + 4;               // 向后移 4 位
        if (s[i] > 'z' || (s[i] > 'Z' && s[i] < 'a'))
        {
            s[i] = s[i] - 26;          // 超出了字母表，绕回开头
        }
    }
    printf("加密后：");
    for (i = 0; i < 5; i++)
    {
        printf("%c", s[i]);
    }
    printf("\n");
    return 0;
}
