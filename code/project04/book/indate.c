/* 程序名：indate.c
   功能：按“年-月-日”的格式输入日期，并查看读入了几个数据 */
#include <stdio.h>

int main(void)
{
    int year = 0, month = 0, day = 0;  // 先赋初值 0
    int n;                             // 成功读入的数据个数

    printf("请输入实训日期（如 2026-10-15）：");
    n = scanf("%d-%d-%d", &year, &month, &day);
    printf("成功读入 %d 个数据\n", n);
    printf("实训日期：%d 年 %d 月 %d 日\n", year, month, day);
    return 0;
}
