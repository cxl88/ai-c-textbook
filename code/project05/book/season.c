/* 程序名：season.c
   功能：输入月份，输出季节和光伏发电的注意事项 */
#include <stdio.h>

int main(void)
{
    int month;                         // 月份

    printf("月份（1～12）：");
    scanf("%d", &month);
    if (month >= 1 && month <= 12)     // 先检查月份是否有效
    {
        switch (month)
        {
        case 3: case 4: case 5:
            printf("春季：日照逐渐增强，发电量上升。\n");
            break;
        case 6: case 7: case 8:
            printf("夏季：日照最强，注意组件散热。\n");
            break;
        case 9: case 10: case 11:
            printf("秋季：天气晴朗，发电较稳定。\n");
            break;
        default:                       // 剩下 12、1、2 月
            printf("冬季：日照时间短，注意清扫积雪。\n");
        }
    }
    else
    {
        printf("月份输入有误。\n");
    }
    return 0;
}
