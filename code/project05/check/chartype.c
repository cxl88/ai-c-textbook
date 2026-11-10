/* 程序名：chartype.c
   功能：实训巩固第 15 题参考答案：判断字符的类别 */
#include <stdio.h>

int main(void)
{
    char c;

    printf("请输入一个字符：");
    c = getchar();
    if (c >= 'A' && c <= 'Z')
    {
        printf("大写字母\n");
    }
    else if (c >= 'a' && c <= 'z')
    {
        printf("小写字母\n");
    }
    else if (c >= '0' && c <= '9')
    {
        printf("数字字符\n");
    }
    else
    {
        printf("其他字符\n");
    }
    return 0;
}
