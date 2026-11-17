/* 程序名：str_func.c
   功能：4 个常用的字符串处理函数 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char a[20] = "Volt";               // 留足空间，后面还要连接
    char b[20];

    printf("a的长度：%d\n", (int)strlen(a));
    strcpy(b, a);                      // 把 a 复制到 b 中
    strcat(a, "age");                  // 把 "age" 连接到 a 的后面
    printf("a：%s  b：%s\n", a, b);
    printf("strcmp(a, b)：%d\n", strcmp(a, b));
    printf("strcmp(b, a)：%d\n", strcmp(b, a));
    printf("strcmp(b, \"Volt\")：%d\n", strcmp(b, "Volt"));
    printf("\"支路正常\"的长度：%d\n", (int)strlen("支路正常"));
    return 0;
}
