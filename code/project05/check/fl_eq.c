/* 程序名：fl_eq.c
   功能：核对“0.1 + 0.2 == 0.3 的值为 0”（关系运算符的易错点③） */
#include <stdio.h>

int main(void)
{
    printf("0.1 + 0.2 == 0.3 的值：%d\n", 0.1 + 0.2 == 0.3);
    printf("0.1 + 0.2 = %.17f\n", 0.1 + 0.2);
    return 0;
}
