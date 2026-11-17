/* 程序名：above_avg.c
   功能：输入 6 位同学的实训成绩，输出平均分和高于平均分的成绩 */
#include <stdio.h>

int main(void)
{
    int score[6];                      // 6 位同学的成绩
    int i, sum = 0;                    // 下标、总分
    float avg;                         // 平均分

    for (i = 0; i < 6; i++)
    {
        printf("请输入第%d位同学的成绩：", i + 1);
        scanf("%d", &score[i]);
        sum = sum + score[i];
    }
    avg = sum / 6.0;
    printf("平均分：%.1f\n", avg);
    printf("高于平均分的成绩：");
    for (i = 0; i < 6; i++)            // 再把 6 个成绩逐个取出来比较
    {
        if (score[i] > avg)
        {
            printf("%d ", score[i]);
        }
    }
    printf("\n");
    return 0;
}
