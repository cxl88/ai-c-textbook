/* 程序名：lamp1_while.c
   功能：用 while 语句改写 lamp1.c（code 要先赋一个不是 0 的值） */
#include <stdio.h>

int main(void)
{
    int code = -1;                     // 先赋一个不是 0 的值，让条件第一次成立
    int n = 0;

    while (code != 0)
    {
        n++;
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
    }
    return 0;
}
