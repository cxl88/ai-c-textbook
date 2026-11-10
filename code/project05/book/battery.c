/* 程序名：battery.c
   功能：电量低于 20% 时提醒充电（单分支） */
#include <stdio.h>

int main(void)
{
    int power;                         // 剩余电量（%）

    printf("剩余电量（%%）：");
    scanf("%d", &power);
    if (power < 20)                    // 电量低于 20% 吗？
    {
        printf("电量不足，请及时充电！\n");
    }
    printf("当前电量：%d%%\n", power);
    return 0;
}
