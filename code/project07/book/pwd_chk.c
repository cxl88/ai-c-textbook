/* 程序名：pwd_chk.c
   功能：统计密码中字母、数字和其他字符的个数，判断密码强度 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char pwd[30];                      // 密码（不含空格）
    char c;                            // 正在检查的字符
    int i, letter = 0, digit = 0, other = 0;

    printf("请输入密码：");
    scanf("%s", pwd);
    for (i = 0; pwd[i] != '\0'; i++)   // 逐个检查，直到 '\0'
    {
        c = pwd[i];
        if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
        {
            letter++;
        }
        else if (c >= '0' && c <= '9')
        {
            digit++;
        }
        else
        {
            other++;
        }
    }
    printf("字母%d个，数字%d个，", letter, digit);
    printf("其他字符%d个\n", other);
    if (strlen(pwd) >= 8 && letter > 0 && digit > 0)
    {
        printf("密码强度：较强\n");
    }
    else
    {
        printf("密码强度：弱（至少 8 位，并且字母、数字都要有）\n");
    }
    return 0;
}
