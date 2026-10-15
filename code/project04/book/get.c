/* 程序名：get.c
   功能：用 getchar 输入一个字符，输出这个字符和它的 ASCII 码 */
#include <stdio.h>

int main(void)
{
    char c;

    printf("请输入电阻状态（Y/N）：");
    c = getchar();                     // 从键盘读入一个字符
    printf("读到的字符：");
    putchar(c);                        // 输出这个字符
    printf("，ASCII 码：%d\n", c);
    return 0;
}
