/* 程序名：bad_nobrace.c
   功能：任务一 课堂练习（while 语句）第 3 题：循环体漏写花括号（死循环，只编译） */
#include <stdio.h>

int main(void)
{
    int i = 0;

    while (i <= 5)
        printf("%d ", i);
        i++;
    return 0;
}
