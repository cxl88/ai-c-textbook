/* 程序名：seat204b.c（参考答案：训练 1 改一项需求）*/
#include <stdio.h>
#define ROOM 204                        // 实训室编号

int main(void)
{
    const int seats = 40;               // 总座位数
    int people = 25;                    // 当前在室人数
    int times = 3;                      // 今日实训场次
    double temp = 23.6;                 // 当前环境温度（℃）
    int empty;                          // 空座位数

    empty = seats - people;
    printf("实训室编号：%d\n", ROOM);
    printf("今日实训场次：%d\n", times);
    printf("空座位数：%d\n", empty);
    printf("当前环境温度：%.1f ℃\n", temp);
    return 0;
}
