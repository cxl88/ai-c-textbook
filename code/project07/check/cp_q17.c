/* 程序名：cp_q17.c
   功能：实训巩固第 17 题参考答案：按成绩从高到低排名 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[5][20], tn[20];          // 姓名、交换姓名用
    int score[5], ts;                  // 成绩、交换成绩用
    int i, j;

    for (i = 0; i < 5; i++)
    {
        printf("请输入第%d位同学的姓名和成绩：", i + 1);
        scanf("%s%d", name[i], &score[i]);
    }
    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 4 - i; j++)
        {
            if (score[j] < score[j + 1])
            {
                ts = score[j];
                score[j] = score[j + 1];
                score[j + 1] = ts;
                strcpy(tn, name[j]);   // 姓名跟着一起交换
                strcpy(name[j], name[j + 1]);
                strcpy(name[j + 1], tn);
            }
        }
    }
    for (i = 0; i < 5; i++)
    {
        printf("第%d名  %s  %d\n", i + 1, name[i], score[i]);
    }
    return 0;
}
