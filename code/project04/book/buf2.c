/* 程序名：buf2.c
   功能：先读走回车符，再用 getchar 读入状态字符 */
#include <stdio.h>

int main(void)
{
    float r;
    char s;

    printf("阻值（kΩ）：");
    scanf("%f", &r);                   // 读入阻值，回车符留在缓冲区中
    getchar();                         // 读走回车符（不保存）
    printf("状态（Y/N）：");
    s = getchar();                     // 这次读到的才是状态字符
    printf("读到的状态字符的 ASCII 码：%d\n", s);
    return 0;
}
