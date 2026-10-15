/* 程序名：dog.c
   功能：输入 3 个字母，倒序输出 */
#include <stdio.h>

int main(void)
{
    char c1, c2, c3;

    printf("请输入 3 个字母：");
    c1 = getchar();                    // ① 依次读入 3 个字母
    c2 = getchar();
    c3 = getchar();
    printf("倒过来是：");
    putchar(c3);                       // ② 倒序输出
    putchar(c2);
    putchar(c1);
    putchar('\n');
    return 0;
}
