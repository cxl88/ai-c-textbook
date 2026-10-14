#include <stdio.h>

int main(void)
{
    int people;                         // 在室人数
    double temp;                        // 温度
    char code;                          // 故障编码
    int n;                              // scanf 的返回值

    printf("请输入人数、温度和故障编码：");
    n = scanf("%d %lf %c", &people, &temp, &code);   // double 用 %lf
    printf("scanf 返回值：%d\n", n);
    if (n != 3)                         // 检查：3 个数据是否都读入了
    {
        printf("输入格式不对，程序结束。\n");
        return 1;
    }
    printf("人数 %d，温度 %.1f，编码 %c\n", people, temp, code);
    return 0;
}
