/* 程序名：bad_wsemi.c
   功能：错误示范——while 的条件后面多写了分号（死循环，不要运行） */
#include <stdio.h>

int main(void)
{
    int i, sum;

    sum = 0;
    i = 1;
    while (i <= 100);                  // 多写了一个分号
    {
        sum = sum + i;
        i++;
    }
    printf("1+2+…+100 = %d\n", sum);
    return 0;
}
