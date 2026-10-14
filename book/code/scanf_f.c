#include <stdio.h>

int main(void)
{
    double temp = 0;                    // 室内温度（℃）
    printf("请输入室内温度：");
    scanf("%f", &temp);                 // 按 AI 的建议：用 %f 读入 double 型变量
    printf("室内温度：%.1f ℃\n", temp);
    return 0;
}
