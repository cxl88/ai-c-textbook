#include <stdio.h>

int main(void)
{
    int people;                         // 在室人数
    printf("请输入在室人数：");
    scanf("%d", people);                // 错误：变量名前漏写了 &
    printf("在室人数：%d\n", people);
    return 0;
}
