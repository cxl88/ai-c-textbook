/* 程序名：put.c
   功能：用 putchar 输出字符 */
#include <stdio.h>

int main(void)
{
    char a = 'O', b = 'K';

    putchar(a);                        // 输出字符变量 a 的值
    putchar(b);
    putchar('!');                      // 输出字符常量
    putchar('\n');                     // 输出换行符
    putchar(89);                       // 89 是字符 Y 的 ASCII 码
    putchar('\n');
    return 0;
}
