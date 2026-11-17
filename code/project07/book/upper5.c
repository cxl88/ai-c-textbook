/* 程序名：upper5.c
   功能：输入 5 个状态码，小写字母统一转成大写后输出 */
#include <stdio.h>

int main(void)
{
    char c[5];                         // 5 个状态码
    int i;

    printf("请输入5个状态码：");
    for (i = 0; i < 5; i++)
    {
        scanf(" %c", &c[i]);           // 先跳过空格和换行符
    }
    for (i = 0; i < 5; i++)
    {
        if (c[i] >= 'a' && c[i] <= 'z')
        {
            c[i] = c[i] - 32;          // 小写字母减 32 得到大写字母
        }
    }
    printf("统一为大写：");
    for (i = 0; i < 5; i++)
    {
        printf("%c ", c[i]);
    }
    printf("\n");
    return 0;
}
