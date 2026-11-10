/* 程序名：scanf_nl.c
   功能：观察格式控制字符串末尾多写 \n 的后果 */
#include <stdio.h>

int main(void)
{
    int n;

    printf("请输入在室人数：");
    scanf("%d\n", &n);                 // 错误写法：末尾多了 \n
    printf("在室人数：%d\n", n);
    return 0;
}
