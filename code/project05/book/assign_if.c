/* 程序名：assign_if.c
   功能：错误示范——把“==”写成了“=” */
#include <stdio.h>

int main(void)
{
    int n;                             // 实训室在室人数

    printf("在室人数：");
    scanf("%d", &n);
    if (n = 0)                         // 本想判断 n 是否等于 0
    {
        printf("实训室无人，请关闭总电源。\n");
    }
    printf("在室人数：%d\n", n);
    return 0;
}
