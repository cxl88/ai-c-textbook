/* 程序名：bad_div0.c
   功能：错误示范——两个条件写反，n 为 0 时先做除数为 0 的整数除法（未定义行为，只编译、不运行） */
#include <stdio.h>

int main(void)
{
    int n, total;                      // 工作的组件块数、总功率（W）

    printf("工作的组件块数：");
    scanf("%d", &n);
    printf("总功率（W）：");
    scanf("%d", &total);
    if (total / n < 80 && n != 0)      // 顺序写反：n 为 0 时先算 total / n
    {
        printf("平均功率偏低，请清洁组件表面！\n");
    }
    else
    {
        printf("暂不需要清洁组件。\n");
    }
    return 0;
}
