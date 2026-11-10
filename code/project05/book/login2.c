/* 程序名：login2.c
   功能：先核对账号，账号正确再核对密码（if 嵌套） */
#include <stdio.h>

int main(void)
{
    int id, pwd;                       // 账号、密码

    printf("账号：");
    scanf("%d", &id);
    if (id == 20260501)                // 外层：账号对吗？
    {
        printf("密码：");
        scanf("%d", &pwd);
        if (pwd == 123456)             // 内层：密码对吗？
        {
            printf("登录成功，欢迎进入教学平台！\n");
        }
        else
        {
            printf("密码错误，请重新输入。\n");
        }
    }
    else
    {
        printf("账号不存在。\n");
    }
    return 0;
}
