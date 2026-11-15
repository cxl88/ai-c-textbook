/* 程序名：ai_a_code.c
   功能：离开 AI 再做 ②参考答案：状态码不是 0、1、2 时提示有误，这一次也不算一盏灯 */
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
        else                           // 0、1、2 以外的整数
        {
            printf("状态码有误，请重新输入！\n");
            n--;
        }
    } while (code != 0);
    return 0;
}
