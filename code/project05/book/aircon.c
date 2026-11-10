/* 程序名：aircon.c
   功能：实训室空调自动控制（if 嵌套） */
#include <stdio.h>

int main(void)
{
    char someone;                      // 室内有没有人：Y/N
    float t;                           // 室内温度（℃）

    printf("室内有人吗（Y/N）：");
    someone = getchar();
    if (someone == 'Y')
    {
        printf("室内温度（℃）：");
        scanf("%f", &t);
        if (t > 26)
        {
            printf("空调：制冷\n");
        }
        else if (t < 18)
        {
            printf("空调：制热\n");
        }
        else
        {
            printf("空调：待机\n");
        }
    }
    else
    {
        printf("室内无人，空调关闭。\n");
    }
    return 0;
}
