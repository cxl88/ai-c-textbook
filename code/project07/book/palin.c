/* 程序名：palin.c
   功能：判断输入的英文单词是不是回文（正读、反读都一样） */
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
