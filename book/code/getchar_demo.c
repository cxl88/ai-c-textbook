#include <stdio.h>

int main(void)
{
    char c;
    printf("请输入一个字母：");
    c = getchar();                      // 从键盘读入一个字符
    printf("你输入的是：");
    putchar(c);                         // 输出一个字符
    putchar('\n');                      // 输出一个换行符
    return 0;
}
