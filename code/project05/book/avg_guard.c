/* 程序名：avg_guard.c
   功能：利用短路求值，避免除数为 0 */
#include <stdio.h>

int main(void)
{
    int n, total;                      // 工作的组件块数、总功率（W）

    printf("工作的组件块数：");
    scanf("%d", &n);
    printf("总功率（W）：");
    scanf("%d", &total);
    if (n != 0 && total / n < 80)      // n 为 0 时，不会计算 total / n
    {
        printf("平均功率偏低，请清洁组件表面！\n");
    }
    else
    {
        printf("暂不需要清洁组件。\n");
    }
    return 0;
}
