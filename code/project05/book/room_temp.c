/* 程序名：room_temp.c
   功能：根据实训室温度给出提示（多分支） */
#include <stdio.h>

int main(void)
{
    float t;                           // 实训室温度（℃）

    printf("实训室温度（℃）：");
    scanf("%f", &t);
    if (t < 18)
    {
        printf("偏冷，请打开暖风。\n");
    }
    else if (t <= 26)
    {
        printf("温度适宜。\n");
    }
    else
    {
        printf("偏热，请打开空调制冷。\n");
    }
    return 0;
}
