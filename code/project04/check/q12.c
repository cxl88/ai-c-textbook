/* 程序名：q12.c
   功能：输入体温和心率，输出健康打卡记录（改正后） */
#include <stdio.h>

int main(void)
{
    double temp;
    int rate;

    printf("请输入体温（℃）和心率（次/分）：");
    scanf("%lf%d", &temp, &rate);
    printf("体温：%.1f ℃，心率：%d 次/分\n", temp, rate);
    return 0;
}
