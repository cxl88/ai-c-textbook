/* 程序名：grade_bad.c
   功能：错误示范——多分支的条件顺序写反了 */
#include <stdio.h>

int main(void)
{
    int score;                         // 考核成绩（0～100）

    printf("实训考核成绩（0～100）：");
    scanf("%d", &score);
    if (score >= 60)
    {
        printf("合格\n");
    }
    else if (score >= 80)
    {
        printf("良好\n");
    }
    else if (score >= 90)
    {
        printf("优秀\n");
    }
    else
    {
        printf("不合格\n");
    }
    return 0;
}
