#include <stdio.h>

int main(void)
{
    int people = 36;            // 在室人数
    double temp = 24.5;         // 环境温度（℃）
    int a, b;

    people += 4;                // 等价于 people = people + 4
    printf("people += 4 后：%d\n", people);
    people -= 2;                // 等价于 people = people - 2
    printf("people -= 2 后：%d\n", people);
    temp -= 0.5;                // 等价于 temp = temp - 0.5
    printf("temp -= 0.5 后：%.1f\n", temp);

    a = b = 10;                 // 先算 b = 10，再把 10 赋给 a
    printf("a = %d，b = %d\n", a, b);
    b *= 2 + 3;                 // 等价于 b = b * (2 + 3)
    printf("b *= 2 + 3 后：b = %d\n", b);
    printf("赋值表达式 a = 5 的值是 %d\n", a = 5);
    return 0;
}
