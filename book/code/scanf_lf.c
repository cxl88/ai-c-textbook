#include <stdio.h>

int main(void)
{
    double temp;                        // 室内温度（℃）
    printf("请输入室内温度：");
    if (scanf("%lf", &temp) != 1)       // 用 %lf 读入，并检查
    {
        printf("输入的不是数，程序结束。\n");
        return 1;
    }
    printf("室内温度：%.1f ℃\n", temp);
    return 0;
}
