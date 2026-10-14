#include <stdio.h>

int main(void)
{
    const int seats = 48;               // 只读变量：总座位数
    seats = 50;                         // 错误：试图修改只读变量
    printf("总座位数：%d\n", seats);
    return 0;
}
