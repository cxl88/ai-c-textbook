/* 程序名：cp_t3.c
   功能：任务三 课堂练习答案核对：break 与 continue 的比较第 2 题、典型示例第 2 题 */
#include <stdio.h>

int main(void)
{
    int i, sum = 0;

    for (i = 1; i <= 10; i++)
    {
        if (i % 2 == 0)
        {
            continue;
        }
        sum = sum + i;
    }
    printf("比较第2题：sum = %d\n", sum);
    printf("典型示例第2题：");
    for (i = 1; i <= 100; i++)
    {
        if (i % 3 == 0 && i % 5 == 0)
        {
            printf("%d ", i);
        }
    }
    printf("\n");
    return 0;
}
