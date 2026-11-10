/* 程序名：bad_else.c
   功能：错误示范——if 的条件后面多写分号，else 找不到配对的 if */
#include <stdio.h>

int main(void)
{
    int score;                         // 考核成绩

    printf("实训考核成绩：");
    scanf("%d", &score);
    if (score >= 60);
    {
        printf("考核通过！\n");
    }
    else
    {
        printf("未通过，请参加补考。\n");
    }
    return 0;
}
