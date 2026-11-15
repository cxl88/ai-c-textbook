/* 程序名：bad_brk.c
   功能：break 易错点①：在不属于循环和 switch 的 if 语句中使用 break（只编译） */
#include <stdio.h>

int main(void)
{
    int code;

    printf("请输入状态码：");
    scanf("%d", &code);
    if (code == 0)
    {
        printf("短路不亮\n");
        break;
    }
    printf("继续巡检\n");
    return 0;
}
