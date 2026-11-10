/* 程序名：cp_grade.c
   功能：核对任务二 课堂练习（if…else if…else 语句）第 1 题 */
#include <stdio.h>

int main(void)
{
    int score;                         // 考核成绩（0～100）

    printf("实训考核成绩（0～100）：");
    scanf("%d", &score);
    if (score >= 90)
    {
        printf("优秀\n");
    }
    else if (score >= 80)              // 能判断到这里，说明 score＜90
    {
        printf("良好\n");
    }
    else if (score >= 60)              // 能判断到这里，说明 score＜80
    {
        printf("合格\n");
    }
    else
    {
        printf("不合格\n");
    }
    return 0;
}
