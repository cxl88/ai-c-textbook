/* 程序名：cp_str.c
   功能：核对课堂练习：字符串与字符数组 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char s[] = "Hello";
    char t[10] = "OK";
    char u[] = "接触不良";
    char w[4] = {'A', 'B', 'C'};

    printf("%d %d\n", (int)sizeof(s), s[5]);
    printf("%d %d\n", (int)strlen(t), (int)sizeof(t));
    printf("%d\n", (int)sizeof(u));
    printf("%s %d\n", w, w[3]);
    return 0;
}
