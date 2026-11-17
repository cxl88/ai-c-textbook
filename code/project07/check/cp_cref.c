/* 程序名：cp_cref.c
   功能：核对课堂练习：字符数组的引用 */
#include <stdio.h>

int main(void)
{
    char c[5] = {'H', 'e', 'l', 'l', 'o'};
    char e[3] = {'a', 'b', 'c'};
    char k[3];
    int i;

    for (i = 4; i >= 0; i--)
    {
        printf("%c", c[i]);
    }
    printf("\n");
    for (i = 0; i < 3; i++)
    {
        printf("%c", e[i] - 32);
    }
    printf("\n");
    for (i = 0; i < 3; i++)
    {
        scanf("%c", &k[i]);
    }
    printf("k[1]的ASCII码：%d\n", k[1]);
    return 0;
}
