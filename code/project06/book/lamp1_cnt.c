/* 程序名：lamp1_cnt.c
   功能：在 lamp1.c 的基础上，统计各种状态的灯各有几盏（任务一 技能训练 2） */
#include <stdio.h>

int main(void)
{
    int code;                          // 状态码
    int n = 0;                         // 第几个指示灯
    int ok = 0, flash = 0;             // 正常点亮、闪烁异常的盏数

    do
    {
        n++;
        printf("请输入第%d个灯的状态码：", n);
        scanf("%d", &code);
        if (code == 1)
        {
            printf("第%d个灯正常点亮\n", n);
            ok++;
        }
        else if (code == 2)
        {
            printf("第%d个灯闪烁异常\n", n);
            flash++;
        }
        else if (code == 0)
        {
            printf("第%d个灯短路不亮\n", n);
        }
    } while (code != 0);
    printf("共监测 %d 盏灯：", n);
    printf("正常 %d 盏，闪烁 %d 盏，短路 1 盏\n", ok, flash);
    return 0;
}
