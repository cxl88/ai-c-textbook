/* 程序名：lab.c
   功能：显示 0203 实训室的数据档案 */
#include <stdio.h>
#define TYPE 'C'                // 符号常量：实训室类型（字符）
#define ROOM "0203"             // 符号常量：实训室编号（字符串）
#define SEATS 48                // 符号常量：总座位数（整数）

int main(void)
{
    int people = 36;            // 整型变量：当前在室人数
    float temp = 24.5;          // 浮点型变量：当前环境温度（℃）
    int empty;                  // 整型变量：空座位数

    empty = SEATS - people;     // 处理：空座位数 = 总座位数 - 在室人数

    printf("====== 0203 实训室数据档案 ======\n");
    printf("实训室类型：%c\n", TYPE);
    printf("编号：%s\n", ROOM);
    printf("总座位数：%d\n", SEATS);
    printf("当前在室人数：%d\n", people);
    printf("当前环境温度：%.1f ℃\n", temp);
    printf("空座位数：%d\n", empty);
    return 0;
}
