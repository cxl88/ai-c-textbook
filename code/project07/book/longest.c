/* 程序名：longest.c
   功能：输入 5 个英文单词，找出最长的一个（任务四 技能训练 3） */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char w[5][20], longest[20];        // 5 个单词、最长的单词
    int i;

    printf("请输入5个英文单词（用空格隔开）：");
    for (i = 0; i < 5; i++)
    {
        scanf("%s", w[i]);
    }
    strcpy(longest, w[0]);
    for (i = 1; i < 5; i++)
    {
        if (strlen(w[i]) > strlen(longest))
        {
            strcpy(longest, w[i]);
        }
    }
    printf("最长的单词：%s，", longest);
    printf("有%d个字母\n", (int)strlen(longest));
    return 0;
}
