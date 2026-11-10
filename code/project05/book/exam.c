/* 程序名：exam.c
   功能：判断实训考核是否通过（双分支） */
#include <stdio.h>

int main(void)
{
    int score;                         // 考核成绩

    printf("实训考核成绩：");
    scanf("%d", &score);
    if (score >= 60)                   // 60 分及以上为通过
    {
        printf("考核通过！\n");
    }
    else
    {
        printf("未通过，请参加补考。\n");
    }
    return 0;
}
