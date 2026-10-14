/* 程序名：bad_206.c（课堂验收用，由教师发给学生）
   功能：显示 206 实训室的部分数据（程序有错误，待诊断） */
#include <stdio.h>

int main(void)
{
    const int seats = 50;               // 总座位数
    int people = 45;                    // 在室人数
    double t1 = 25.2, t2 = 26.0;        // 上午、下午的室内温度（℃）
    double avg;                         // 平均温度（℃）
    double volt = 219.5;                // 供电电压（V）

    seats = 52;                         // 新增了 2 个座位
    avg = t1 + t2 / 2;                  // 计算平均温度
    printf("在室人数：%d  总座位：%d\n", people, seats);
    printf("平均温度：%.1f ℃\n", avg);
    printf("供电电压：%d V\n", volt);
    return 0;
}
