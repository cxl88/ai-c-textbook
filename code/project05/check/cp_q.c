/* 程序名：cp_q.c
   功能：核对实训巩固第 2、6、8、10 题 */
#include <stdio.h>

int main(void)
{
    int a = 3, b = 4, x, y, m;

    printf("第2题：%d\n", 3 < 5 < 2);
    printf("第6题：%d\n", a > b || a + 1 == b);
    x = 85;
    y = 0;
    if (x >= 90) y = 4; else if (x >= 80) y = 3; else if (x >= 60) y = 2; else y = 1;
    printf("第8题：%d\n", y);
    a = 5;
    b = 3;
    m = a < b ? a : b;
    printf("第10题：%d\n", m);
    return 0;
}
