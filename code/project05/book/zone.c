/* 程序名：zone.c
   功能：输入实训区字母，输出该区的实训内容（switch 语句） */
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
        break;
    case 'B':
        printf("B 区：电子装配实训\n");
        break;
    case 'C':
        printf("C 区：光伏发电实训\n");
        break;
    case 'D':
        printf("D 区：智能控制实训\n");
        break;
    default:
        printf("没有这个实训区，请检查输入。\n");
    }
    return 0;
}
