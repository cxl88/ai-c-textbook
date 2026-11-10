/* 程序名：charge_pile.c
   功能：充电桩启动判断（if 嵌套） */
#include <stdio.h>

int main(void)
{
    char gun;                          // 充电枪是否插好：Y/N
    int soc;                           // 车辆电量（%）

    printf("充电枪插好了吗（Y/N）：");
    gun = getchar();
    if (gun == 'Y')
    {
        printf("车辆电量（%%）：");
        scanf("%d", &soc);
        if (soc < 100)
        {
            printf("开始充电。\n");
        }
        else
        {
            printf("电量已满，无需充电。\n");
        }
    }
    else
    {
        printf("请先插好充电枪！\n");
    }
    return 0;
}
