/* 程序名：scanf_msg.c
   功能：观察把提示文字写进 scanf 的后果 */
#include <stdio.h>

int main(void)
{
    int n = 0;                         // 先赋初值 0

    scanf("请输入人数：%d", &n);       // 错误写法：提示文字不会显示
    printf("n = %d\n", n);
    return 0;
}
