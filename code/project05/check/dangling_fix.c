/* 程序名：dangling_fix.c
   功能：给 dangling.c 加上花括号，让 else 与第一个 if 配对 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("电压（V）：");
    scanf("%f", &v);
    if (v > 21)
    {
        if (v > 24)
        {
            printf("紧急告警，立即停机保护！\n");
        }
    }
    else
    {
        printf("电压没有过压。\n");
    }
    return 0;
}
