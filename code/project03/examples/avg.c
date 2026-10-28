#include <stdio.h>

int main(void)
{
    float c, math, eng;             // 数据：三门课的成绩
    float total, avg;               // 数据：总分和平均分

    c = 86;                         // 步骤1：成绩赋值
    math = 92;
    eng = 78;
    total = c + math + eng;         // 步骤2：求总分
    avg = total / 3;                // 步骤3：求平均分
    printf("总分：%.1f\n", total);  // 步骤4：输出结果
    printf("平均分：%.1f\n", avg);
    return 0;
}
