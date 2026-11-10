/* 程序名：bad_switch_f.c
   功能：错误示范——用 switch 直接判断实型的电压 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("电压（V）：");
    scanf("%f", &v);
    switch (v)
    {
    case 18:
        printf("额定电压。\n");
        break;
    default:
        printf("不是额定电压。\n");
    }
    return 0;
}
