/* 程序名：cp_zone_c.c
   功能：核对任务二 课堂练习（switch 语句）第 1 题：漏写 break 时输入 C */
#include <stdio.h>

int main(void)
{
    char area;                         // 实训区：A～D

    printf("实训区（A～D）：");
    area = getchar();
    switch (area)
    {
    case 'A':
        printf("A 区：电工基础实训\n");
    case 'B':
        printf("B 区：电子装配实训\n");
    case 'C':
        printf("C 区：光伏发电实训\n");
    case 'D':
        printf("D 区：智能控制实训\n");
    default:
        printf("没有这个实训区，请检查输入。\n");
    }
    return 0;
}
