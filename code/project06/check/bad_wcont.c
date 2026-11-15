/* 程序名：bad_wcont.c
   功能：continue 易错点②：在 while 中，continue 跳过了 i++（死循环，只编译） */
#include <stdio.h>

int main(void)
{
    int i = 1;

    while (i <= 20)
    {
        if (i % 3 == 0)
        {
            continue;                  // 跳过了后面的 i++
        }
        printf("%d ", i);
        i++;
    }
    printf("\n");
    return 0;
}
