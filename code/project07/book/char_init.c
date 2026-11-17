/* 程序名：char_init.c
   功能：字符数组初始化的几种情况 */
#include <stdio.h>

int main(void)
{
    char a[5] = {'A', 'B', 'C', 'D', 'E'};  // 全部赋初值
    char b[5] = {'O', 'K'};                 // 部分赋初值，其余为 '\0'
    char c[] = {'H', 'i', '!'};             // 省略长度：3 个元素
    int i;

    for (i = 0; i < 5; i++)
    {
        printf("%c", a[i]);
    }
    printf("\n");
    for (i = 0; i < 5; i++)
    {
        printf("%d ", b[i]);           // 输出各元素的 ASCII 码
    }
    printf("\n");
    for (i = 0; i < 3; i++)
    {
        printf("%c", c[i]);
    }
    printf("\n");
    return 0;
}
