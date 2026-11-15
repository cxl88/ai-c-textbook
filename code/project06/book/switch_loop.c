/* 程序名：switch_loop.c
   功能：错误示范——想用 switch 中的 break 结束循环 */
#include <stdio.h>

int main(void)
{
    int n, code;

    printf("请依次输入 5 盏灯的状态码：");
    for (n = 1; n <= 5; n++)
    {
        scanf("%d", &code);
        switch (code)
        {
        case 0:
            printf("第%d个灯短路不亮\n", n);
            break;                     // 只结束 switch，不结束 for
        case 1:
            printf("第%d个灯正常点亮\n", n);
            break;
        case 2:
            printf("第%d个灯闪烁异常\n", n);
            break;
        }
    }
    return 0;
}
