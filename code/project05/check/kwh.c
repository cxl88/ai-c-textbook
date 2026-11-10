/* 程序名：kwh.c
   功能：任务二 课堂练习（if…else if…else 语句）第 3 题参考答案：用电量分档 */
#include <stdio.h>

int main(void)
{
    int kwh;                           // 月用电量（度）

    printf("月用电量（度）：");
    scanf("%d", &kwh);
    if (kwh <= 200)
    {
        printf("第一档\n");
    }
    else if (kwh <= 400)
    {
        printf("第二档\n");
    }
    else
    {
        printf("第三档\n");
    }
    return 0;
}
