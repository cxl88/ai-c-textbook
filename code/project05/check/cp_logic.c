/* 程序名：cp_logic.c
   功能：核对任务一 课堂练习（逻辑运算符）第 1、3、4 题和课堂活动 */
#include <stdio.h>

int main(void)
{
    int a = 0, b = 2;
    float v;

    printf("第1题：%d %d %d %d\n", !a, a && b, a || b, !b || a);
    v = 18;
    printf("第3题：v=18 时 %d\n", v < 15 || v > 21);
    printf(" v    v<15||v>21  !(v>=15&&v<=21)  v>=15&&v<=21\n");
    v = 14;
    printf("%4.1f %8d %15d %15d\n", v, v < 15 || v > 21, !(v >= 15 && v <= 21), v >= 15 && v <= 21);
    v = 15;
    printf("%4.1f %8d %15d %15d\n", v, v < 15 || v > 21, !(v >= 15 && v <= 21), v >= 15 && v <= 21);
    v = 21;
    printf("%4.1f %8d %15d %15d\n", v, v < 15 || v > 21, !(v >= 15 && v <= 21), v >= 15 && v <= 21);
    v = 22;
    printf("%4.1f %8d %15d %15d\n", v, v < 15 || v > 21, !(v >= 15 && v <= 21), v >= 15 && v <= 21);
    v = 30;
    printf("%4.1f %8d %15d %15d\n", v, v < 15 || v > 21, !(v >= 15 && v <= 21), v >= 15 && v <= 21);
    return 0;
}
