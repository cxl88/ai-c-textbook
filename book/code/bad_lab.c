/* 程序名：bad_lab.c
   功能：显示 203 实训室的完整数据档案（某同学的初稿） */
#include <stdio.h>
#define BUILDING 6                      // 楼栋号

int main(void)
{
    const int room = 203;               // 实训室编号
    const int seats = 48;               // 总座位数
    char type = 'C';                    // 实训室类型
    int people = 36;                    // 实时在室人数
    int times = 3;                      // 今日实训场次
    int faults = 1;                     // 设备故障次数
    int temp = 24.5;                    // 室内环境温度（℃）
    float wet = 56.2;                   // 空气湿度（%）
    char volt = 220;                    // 实际供电电压（V）
    _Bool power = 1;                    // 设备开关机状态
    char code = "g";                    // 故障编码
    double rate;                        // 座位使用率（%）

    room = 204;                         // 想顺便改成 204 实训室
    rate = people / seats * 100;        // 计算座位使用率

    printf("%d号楼 %d 实训室（类型 %c）\n", BUILDING, room, type);
    printf("在室人数：%d  今日场次：%d  故障次数：%d\n", people, times, faults);
    printf("室内温度：%d ℃\n", temp);
    printf("空气湿度：%d%%\n", wet);
    printf("供电电压：%d V\n", volt);
    printf("开关机状态：%d\n", power);
    printf("故障编码：%c\n", code);
    printf("座位使用率：%.1f%%\n", rate);
    return 0;
}
