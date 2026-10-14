/* 程序名：lab206_mid.c（bad_206.c 只改正了编译提示指出的问题，仍有逻辑错误）
   功能：显示 206 实训室的部分数据 */
#include <stdio.h>

int main(void)
{
    const int seats = 52;               // 总座位数
    int people = 45;                    // 在室人数
    double t1 = 25.2, t2 = 26.0;        // 上午、下午的室内温度（℃）
    double avg;                         // 平均温度（℃）
    double volt = 219.5;                // 供电电压（V）

    avg = t1 + t2 / 2;                  // 计算平均温度
    printf("在室人数：%d  总座位：%d\n", people, seats);
    printf("平均温度：%.1f ℃\n", avg);
    printf("供电电压：%.1f V\n", volt);
    return 0;
}
