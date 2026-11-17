/* 程序名：cp_q.c
   功能：核对实训巩固第 7～10 题 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    int a[5] = {1, 2};
    int m[3][4];
    char s[] = "abc";
    char s1[] = "OK", s2[] = "OK";

    printf("第7题：a[2] = %d\n", a[2]);
    printf("第8题：%d 个元素\n", (int)(sizeof(m) / sizeof(m[0][0])));
    printf("第9题：%d 个元素\n", (int)sizeof(s));
    printf("第10题：strcmp = %d\n", strcmp(s1, s2));
    return 0;
}
