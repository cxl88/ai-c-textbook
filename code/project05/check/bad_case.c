/* 程序名：bad_case.c
   功能：任务二 课堂练习（switch 语句）第 2 题：switch 与 case 的错误写法（只编译） */
#include <stdio.h>

int main(void)
{
    float v = 18;
    int n = 5;

    switch (v)
    {
    case 18.0:
        printf("额定");
    }
    switch (n)
    {
    case n > 0:
        printf("正数");
    }
    return 0;
}
