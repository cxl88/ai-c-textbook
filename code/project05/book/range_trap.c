/* 程序名：range_trap.c
   功能：错误示范——把数学中的 15≤v≤21 直接写进程序 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("电压（V）：");
    scanf("%f", &v);
    if (15 <= v <= 21)                 // 想表示“v 在 15～21 之间”
    {
        printf("电压正常。\n");
    }
    return 0;
}
