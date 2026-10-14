#include <stdio.h>

int main(void)
{
    double temp;                        // 室内温度（℃）
    printf("请输入室内温度：");
    scanf("%f", &temp);                 // 按 AI 的建议用 %f 读入
    printf("室内温度：%.1f ℃\n", temp);
    return 0;
}
