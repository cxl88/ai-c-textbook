/* 程序名：soc.c
   功能：储能电池电量分级提示 */
#include <stdio.h>

int main(void)
{
    int soc;                           // 剩余电量（%）

    printf("储能电池剩余电量（%%）：");
    scanf("%d", &soc);
    if (soc >= 80)
    {
        printf("电量充足。\n");
    }
    else if (soc >= 20)
    {
        printf("电量正常。\n");
    }
    else
    {
        printf("电量不足，请及时充电！\n");
    }
    return 0;
}
