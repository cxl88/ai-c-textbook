/* 程序名：bad_cont.c
   功能：continue 易错点①：在不在循环中的 switch 语句中使用 continue（只编译） */
#include <stdio.h>

int main(void)
{
    int code;

    printf("请输入状态码：");
    scanf("%d", &code);
    switch (code)
    {
    case 2:
        printf("闪烁异常\n");
        continue;
    default:
        printf("其他状态\n");
    }
    return 0;
}
