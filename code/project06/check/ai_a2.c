/* 程序名：ai_a2.c
   功能：在办法①的基础上，输入结束（读到 EOF）时结束监测（选学） */
#include <stdio.h>

int main(void)
{
    int code, ch, r;
    int n = 0;

    do
    {
        n++;
        printf("请输入第%d个灯的状态码：", n);
        r = scanf("%d", &code);        // r：成功读入的数据个数
        if (r == EOF)                  // 输入已经结束
        {
            printf("输入已结束\n");
            break;
        }
        if (r != 1)
        {
            printf("输入有误，请重新输入！\n");
            ch = getchar();
            while (ch != '\n' && ch != EOF)
            {
                ch = getchar();
            }
            n--;
            code = -1;
        }
        else if (code == 1)
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
    } while (code != 0);
    return 0;
}
