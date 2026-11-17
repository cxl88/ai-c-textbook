/* 程序名：cp_q16.c
   功能：实训巩固第 16 题参考答案：小写字母转换为大写 */
#include <stdio.h>

int main(void)
{
    char s[50];
    int i;

    printf("请输入一个字符串：");
    scanf("%s", s);
    for (i = 0; s[i] != '\0'; i++)
    {
        if (s[i] >= 'a' && s[i] <= 'z')
        {
            s[i] = s[i] - 32;
        }
    }
    printf("%s\n", s);
    return 0;
}
