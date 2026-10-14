/* 程序名：fix205.c
   功能：显示 205 实训室的部分数据（程序有错误，待诊断） */
#include <stdio.h>

int main(void)
{
    int people = 35;                    // 在室人数
    const int seats = 48;               // 总座位数
    int temp = 25.6;                    // 室内温度（℃），保留 1 位小数
    char code = 'n';                    // 故障编码
    double rate = people / seats * 100.0;   // 座位使用率（%）

    printf("温度：%d ℃\n", temp);
    printf("故障编码：%d\n", code);
    printf("座位使用率：%.1f%%\n", rate);
    return 0;
}
