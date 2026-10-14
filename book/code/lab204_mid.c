/* 程序名：lab204_mid.c（bad_204.c 只改正了编译提示指出的问题，仍有逻辑错误）
   功能：显示 204 实训室的部分数据 */
#include <stdio.h>

int main(void)
{
    const int seats = 40;               // 总座位数
    int people = 30;                    // 在室人数
    double temp = 23.8;                 // 室内温度（℃）
    char type = 'B';                    // 实训室类型
    double rate;                        // 座位使用率（%）

    rate = people / seats * 100;        // 计算座位使用率
    printf("实训室类型：%c\n", type);
    printf("室内温度：%.1f ℃\n", temp);
    printf("座位使用率：%.1f%%\n", rate);
    return 0;
}
