/* 程序名：env.c
   功能：温度高于 30 ℃ 或湿度高于 70% 时提示环境异常 */
#include <stdio.h>

int main(void)
{
    float t, h;                        // 温度（℃）、湿度（%）

    printf("请输入温度（℃）和湿度（%%），用空格隔开：");
    scanf("%f%f", &t, &h);
    if (t > 30 || h > 70)
    {
        printf("环境异常，请开启空调除湿！\n");
    }
    printf("温度 %.1f ℃，湿度 %.0f%%\n", t, h);
    return 0;
}
