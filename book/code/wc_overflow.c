#include <stdio.h>

int main(void)
{
    char a = 220;                       // char 只能保存 -128～127
    char b = 380;                       // 超出得更多
    short c = 40000;                    // short 只能保存 -32768～32767

    printf("a = %d\n", a);
    printf("b = %d\n", b);
    printf("c = %d\n", c);
    return 0;
}
