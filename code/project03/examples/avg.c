/* 程序名：avg.c
   功能：输入三门课的成绩，求总分和平均分 */
#include <stdio.h>

int main(void)
{
    float c, math, eng;      // 数据：三门课的成绩
    float total, avg;        // 数据：总分和平均分

    printf("请输入C语言、高数、英语成绩：");
    scanf("%f%f%f", &c, &math, &eng);         // 步骤1：输入成绩
    total = c + math + eng;                   // 步骤2：求总分
    avg = total / 3;                          // 步骤3：求平均分
    printf("总分：%.1f\n", total);            // 步骤4：输出结果
    printf("平均分：%.1f\n", avg);
    return 0;
}
