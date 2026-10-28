#include <stdio.h>

int main(void)
{
    int id, pwd;

    printf("账号：");
    scanf("%d", &id);
    printf("密码：");
    scanf("%d", &pwd);
    if (id == 20260501 && pwd == 123456)      // 两项都正确吗？
    {
        printf("登录成功，欢迎进入教学平台！\n");
    }
    else
    {
        printf("账号或密码错误，请重新输入。\n");
    }
    printf("（本次操作结束）\n");
    return 0;
}
