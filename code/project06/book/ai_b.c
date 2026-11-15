/* 程序名：ai_b.c
   功能：AI 给出的办法②：每次读入之前，先把 code 设为 0 */
#include <stdio.h>

int main(void)
{
    int code;
    int n = 0;

    do
    {
        n++;
        code = 0;                      // 读入失败时，code 就是 0
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
    } while (code != 0);
    return 0;
}
