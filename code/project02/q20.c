/* 程序名：q20.c
   功能：用 / 和 % 拆分房间号（第 20 题参考答案） */
#include <stdio.h>

int main(void)
{
    int room = 6203;                    // 房间号
    int building, floor, num;           // 楼号、层号、室号

    building = room / 1000;
    floor = room / 100 % 10;
    num = room % 100;
    printf("%d 号楼 %d 层 %d 室\n", building, floor, num);
    return 0;
}
