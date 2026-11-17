/* 程序名：quiz10.c
   功能：10 道选择题自动判分（任务三 技能训练 3） */
#include <stdio.h>

int main(void)
{
    char key[10] = {'B', 'A', 'D', 'C', 'C', 'A', 'B', 'D', 'A', 'C'};
    char ans[10];                      // 学生的答案
    int i, score = 0;

    printf("请输入10道题的答案：");
    for (i = 0; i < 10; i++)
    {
        scanf(" %c", &ans[i]);
    }
    printf("答错的题：");
    for (i = 0; i < 10; i++)
    {
        if (ans[i] == key[i])
        {
            score = score + 10;
        }
        else
        {
            printf("第%d题 ", i + 1);
        }
    }
    printf("\n得分：%d\n", score);
    return 0;
}
