/* 程序名：resok.c
   功能：判断标称 4.7 kΩ、误差 ±5% 的电阻是否合格（双分支） */
#include <stdio.h>

int main(void)
{
    float r;                           // 测得的阻值（kΩ）

    printf("测得的阻值（kΩ）：");
    scanf("%f", &r);
    if (r >= 4.465 && r <= 4.935)      // 4.7×(1−5%)～4.7×(1+5%)
    {
        printf("合格。\n");
    }
    else
    {
        printf("不合格，请更换电阻。\n");
    }
    return 0;
}
