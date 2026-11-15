/* 程序名：ai_c.c
   功能：AI 给出的办法③：把读入写进循环条件 */
#include <stdio.h>

int main(void)
{
    int code;
    int n = 1;

    printf("请输入第%d个灯的状态码：", n);
    while (scanf("%d", &code) == 1 && code != 0)
    {
        if (code == 1)
        {
            printf("第%d个灯正常点亮\n", n);
        }
        else if (code == 2)
        {
            printf("第%d个灯闪烁异常\n", n);
        }
        n++;
        printf("请输入第%d个灯的状态码：", n);
    }
    return 0;
}
