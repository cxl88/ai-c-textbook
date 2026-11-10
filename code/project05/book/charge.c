/* 程序名：charge.c
   功能：蓄电池温度超出 0～45 ℃ 时暂停充电 */
#include <stdio.h>

int main(void)
{
    float t;                           // 蓄电池温度（℃）

    printf("蓄电池温度（℃）：");
    scanf("%f", &t);
    if (t < 0 || t > 45)               // 低于 0 ℃ 或高于 45 ℃
    {
        printf("温度超出 0～45 ℃，暂停充电！\n");
    }
    printf("检测完毕。\n");
    return 0;
}
