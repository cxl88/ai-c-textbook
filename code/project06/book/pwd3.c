/* 程序名：pwd3.c
   功能：最多输入 3 次密码，输对就登录，3 次都错就锁定（任务三 技能训练 1） */
#include <stdio.h>

int main(void)
{
    int pwd, i;

    for (i = 1; i <= 3; i++)
    {
        printf("请输入密码（第%d次）：", i);
        scanf("%d", &pwd);
        if (pwd == 123456)             // 密码正确（数据为虚构）
        {
            printf("登录成功！\n");
            break;                     // 不必再输入，结束循环
        }
        printf("密码错误。\n");
    }
    if (i > 3)                         // 3 次都没有输对
    {
        printf("密码错误已达 3 次，账号锁定。\n");
    }
    return 0;
}
