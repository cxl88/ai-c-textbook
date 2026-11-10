/* 程序名：stmt.c
   功能：认识 C 语言的五类语句 */
#include <stdio.h>

int main(void)
{
    int a, b, sum;                     // 定义变量（属于声明）

    a = 3;                             // 表达式语句（赋值语句）
    b = 5;                             // 表达式语句（赋值语句）
    ;                                  // 空语句：什么也不做
    {                                  // 复合语句：用 { } 括起来
        sum = a + b;                   //   表达式语句（赋值语句）
        printf("sum = %d\n", sum);     //   函数调用语句
    }
    return 0;                          // 控制语句：结束 main 函数
}
