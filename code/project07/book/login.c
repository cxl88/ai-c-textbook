/* 程序名：login.c
   功能：输入用户名和密码，都正确才能登录（任务四 技能训练 1） */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char user[20], pwd[20];            // 用户名、密码

    printf("用户名：");
    scanf("%s", user);
    printf("密码：");
    scanf("%s", pwd);
    if (strcmp(user, "linxh") == 0 && strcmp(pwd, "Lab2026") == 0)
    {
        printf("登录成功！\n");
    }
    else
    {
        printf("用户名或密码错误！\n");
    }
    return 0;
}
