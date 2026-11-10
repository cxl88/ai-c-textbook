/* 程序名：cp_order.c
   功能：核对任务二 课堂练习（if…else if…else 语句）第 2 题 */
#include <stdio.h>

int main(void)
{
    float t = 35;

    if (t > 20) printf("暖"); else if (t > 30) printf("热"); else printf("冷");
    printf("\n");
    return 0;
}
