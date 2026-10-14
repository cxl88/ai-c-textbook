/* 程序名：lab210.c（参考答案）
   功能：显示 210 实训室完整、规范的数据档案 */
#include <stdio.h>
#define BUILDING 6                      // 楼栋号（符号常量）

int main(void)
{
    const int room = 210;               // 实训室编号：201～210
    const int seats = 40;               // 总座位数
    char type = 'B';                    // 实训室类型：'A'～'Z'
    int people = 32;                    // 实时在室人数：0～40
    int times = 2;                      // 今日实训场次
    int faults = 0;                     // 设备故障次数
    double temp = 26.3;                 // 室内环境温度（℃），1 位小数
    double wet = 61.5;                  // 空气湿度（%），1 位小数
    double volt = 219.6;                // 实际供电电压（V）：0～380
    _Bool power = 1;                    // 设备开关机状态：1 开机，0 关机
    char code = 'k';                    // 故障编码：'g'～'n'
    int empty;                          // 空座位数
    double rate;                        // 座位使用率（%）
    char secret;                        // 故障编码的加密报文

    empty = seats - people;
    rate = (double)people / seats * 100;
    secret = code - 32 + 1;

    printf("====== %d号楼 %d 实训室 ======\n", BUILDING, room);
    printf("类型：%c  总座位：%d  空座位：%d\n", type, seats, empty);
    printf("在室人数：%d  座位使用率：%.1f%%\n", people, rate);
    printf("今日场次：%d  故障次数：%d\n", times, faults);
    printf("室内温度：%.1f ℃  空气湿度：%.1f%%\n", temp, wet);
    printf("供电电压：%.1f V  开关机状态：%d\n", volt, power);
    printf("故障编码：%c  加密报文：%c\n", code, secret);
    return 0;
}
