/* 程序名：cp_pal.c
   功能：核对课堂练习和“想一想”：几个单词是不是回文 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char s[30];
    int i, j;                          // 从两头向中间比较的下标

    printf("请输入一个英文单词：");
    scanf("%s", s);
    i = 0;
    j = strlen(s) - 1;                 // 最后一个字符的下标
    while (i < j && s[i] == s[j])
    {
        i++;
        j--;
    }
    if (i >= j)                        // 一直比较到中间都相同
    {
        printf("%s 是回文\n", s);
    }
    else
    {
        printf("%s 不是回文\n", s);
    }
    return 0;
}
