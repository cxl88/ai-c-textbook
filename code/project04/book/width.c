/* 程序名：width.c
   功能：观察输出宽度和小数位数的效果（用方括号看清空格） */
#include <stdio.h>

int main(void)
{
    int n = 25;
    float r = 4.7;

    printf("[%d]\n", n);       // 按实际位数输出
    printf("[%5d]\n", n);      // 至少占 5 列，右对齐，左边补空格
    printf("[%-5d]\n", n);     // 至少占 5 列，左对齐，右边补空格
    printf("[%1d]\n", n);      // 宽度不够时，按实际位数全部输出
    printf("[%05d]\n", n);     // 左边补 0（选学）
    printf("[%f]\n", r);       // 默认 6 位小数
    printf("[%.2f]\n", r);     // 保留 2 位小数
    printf("[%8.2f]\n", r);    // 占 8 列（含小数点），保留 2 位小数
    printf("[%-8.2f]\n", r);   // 左对齐
    return 0;
}
