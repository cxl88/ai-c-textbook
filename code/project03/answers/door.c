/* 技能训练 3（任务二）参考：门禁密码最多输入 3 次（数据为虚构） */
#include <stdio.h>

int main(void)
{
    int times, pwd, ok;

    times = 0;                       // 已经输入的次数
    ok = 0;                          // 0 表示还没输对
    while (times < 3 && ok == 0)
    {
        printf("请输入 6 位密码：");
        scanf("%d", &pwd);
        times = times + 1;
        if (pwd == 203203)
        {
            ok = 1;
        }
        else
        {
            printf("密码错误（已错 %d 次）\n", times);
        }
    }
    if (ok == 1)
    {
        printf("密码正确，门已打开\n");
    }
    else
    {
        printf("连续 3 次错误，门禁锁定并报警！\n");
    }
    return 0;
}
