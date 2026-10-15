#include <stdio.h>

int main(void)
{
    float km, minutes, pace;

    pace = minutes / km;
    printf("跑步距离（千米）：");
    scanf("%f", &km);
    printf("用时（分钟）：");
    scanf("%f", &minutes);
    printf("平均配速：%.2f 分钟/千米\n", pace);
    return 0;
}
