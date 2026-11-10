/* 程序名：grade_sw2.c
   功能：任务二 课堂练习（switch 语句）第 3 题参考答案：先检查成绩范围，再用 switch */
#include <stdio.h>

int main(void)
{
    int score;                         // 考核成绩（0～100）

    printf("实训考核成绩（0～100）：");
    scanf("%d", &score);
    if (score < 0 || score > 100)
    {
        printf("成绩输入有误。\n");
    }
    else
    {
        switch (score / 10)
        {
        case 10:
        case 9:
            printf("优秀\n");
            break;
        case 8:
            printf("良好\n");
            break;
        case 7:
        case 6:
            printf("合格\n");
            break;
        default:
            printf("不合格\n");
        }
    }
    return 0;
}
