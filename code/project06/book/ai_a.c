/* 程序名：ai_a.c
   功能：AI 给出的办法①：检查 scanf 的返回值，读入失败时读走这一行 */
#include <stdio.h>

int main(void)
{
    int code, ch;
    int n = 0;

    do
    {
        n++;
        printf("请输入第%d个灯的状态码：", n);
        if (scanf("%d", &code) != 1)   // 没有读入一个整数
        {
            printf("输入有误，请重新输入！\n");
            ch = getchar();            // 读走这一行剩下的字符
            while (ch != '\n' && ch != EOF)
            {
                ch = getchar();
            }
            n--;                       // 这一次不算一盏灯
            code = -1;                 // 不是 0，循环继续
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
