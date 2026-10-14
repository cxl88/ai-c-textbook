/* 程序名：lab.c
   功能：显示 203 实训室的当前数据档案 */
#include <stdio.h>
#define TYPE 'C'                        // 符号常量：实训室类型（字符型）
#define ROOM 203                        // 符号常量：实训室编号（整型）

int main(void)
{
    const int seats = 48;               // 只读变量：总座位数
    int people = 48;                    // 整型变量：当前在室人数
    double temp = 24.5;                 // 浮点型变量：当前环境温度（℃）
    _Bool power = 1;                    // 布尔型变量：教师计算机是否开机
    int empty;                          // 整型变量：空座位数

    empty = seats - people;             // 空座位数 = 总座位数 - 在室人数

    printf("====== 203 实训室数据档案 ======\n");
    printf("实训室类型：%c\n", TYPE);
    printf("实训室编号：%d\n", ROOM);
    printf("总座位数：%d\n", seats);
    printf("当前在室人数：%d\n", people);
    printf("当前环境温度：%.1f ℃\n", temp);
    printf("教师计算机开机：%d（1 开机，0 关机）\n", power);
    printf("空座位数：%d\n", empty);
    return 0;
}
