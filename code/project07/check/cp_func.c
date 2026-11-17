/* 程序名：cp_func.c
   功能：核对课堂练习：字符串处理函数 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char a[20] = "AI";
    char x[] = "abc", y[] = "abd";

    printf("%d %d\n", (int)strlen("ABC"), (int)sizeof("ABC"));
    strcat(a, "助教");
    printf("%s %d\n", a, (int)strlen(a));
    printf("%d\n", strcmp(x, y));
    return 0;
}
