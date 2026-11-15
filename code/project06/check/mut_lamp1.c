/* 程序名：mut_lamp1.c
   功能：课堂验收（任务一）：把循环条件改成 code == 0 */
#include <stdio.h>

int main(void)
{
    int code;                          // 状态码
    int n = 0;                         // 第几个指示灯

    do
    {
        n++;                           // 准备读下一个灯
        printf("请输入第%d个灯的状态码：", n);
        scanf("%d", &code);
        if (code == 1)
        {
            printf("第%d个灯正常点亮\n", n);
        }
        else if (code == 2)
        {
            printf("第%d个灯闪烁异常\n", n);
        }
        else if (code == 0)
        {
            printf("第%d个灯短路不亮\n", n);
        }
    } while (code == 0);               // 状态码不是 0，就继续监测
    return 0;
}
