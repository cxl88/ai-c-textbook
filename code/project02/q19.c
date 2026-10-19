/* 程序名：q19.c
   功能：输出 0205 实训室的空座位数和座位利用率（第 19 题参考答案） */
#include <stdio.h>

int main(void)
{
    int seats = 42, people = 35;        // 总座位数、在室人数
    int empty;                          // 空座位数
    double rate;                        // 座位利用率（%）

    empty = seats - people;
    rate = (double)people / seats * 100;
    printf("空座位数：%d\n", empty);
    printf("座位利用率：%.1f%%\n", rate);
    return 0;
}
