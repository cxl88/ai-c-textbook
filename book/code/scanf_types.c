#include <stdio.h>

int main(void)
{
    int people;                         // 在室人数
    double temp;                        // 温度
    char code;                          // 故障编码

    printf("请输入人数、温度和故障编码：");
    scanf("%d %lf %c", &people, &temp, &code);   // double 用 %lf 读入
    printf("人数 %d，温度 %.1f，编码 %c\n", people, temp, code);
    return 0;
}
