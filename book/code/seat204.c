#include <stdio.h>
#define ROOM 204                        // 实训室编号

int main(void)
{
    const int seats = 40;               // 总座位数
    int people = 25;                    // 当前在室人数
    int times = 3;                      // 今日实训场次
    int empty;                          // 空座位数

    empty = seats - people;
    printf("实训室编号：%d\n", ROOM);
    printf("今日实训场次：%d\n", times);
    printf("空座位数：%d\n", empty);
    return 0;
}
