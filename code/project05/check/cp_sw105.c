/* 程序名：cp_sw105.c
   功能：核对任务二 课堂练习（switch 语句）第 3 题：输入 105 */
#include <stdio.h>

int main(void)
{
    int score;                         // 考核成绩（0～100）

    printf("实训考核成绩（0～100）：");
    scanf("%d", &score);
    switch (score / 10)                // 整数相除，得到十位上的数字
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
    return 0;
}
