/* 程序名：buf.c
   功能：观察 scanf 之后用 getchar 读到的是什么 */
#include <stdio.h>

int main(void)
{
    float r;
    char s;

    printf("阻值（kΩ）：");
    scanf("%f", &r);                   // 读入阻值，回车符留在缓冲区中
    printf("状态（Y/N）：");
    s = getchar();                     // 读到的是什么？
    printf("读到的状态字符的 ASCII 码：%d\n", s);
    return 0;
}
