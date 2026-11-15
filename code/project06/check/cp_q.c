/* 程序名：cp_q.c
   功能：核对实训巩固第 6、7、8、10 题 */
#include <stdio.h>

int main(void)
{
    int i, j, s, n;

    i = 1;
    s = 0;
    while (i <= 10)
    {
        s = s + i;
        i = i + 2;
    }
    printf("第6题：s = %d\n", s);
    n = 0;
    for (i = 0; i < 10; i += 2)
    {
        n++;
    }
    printf("第7题：%d 次\n", n);
    printf("第8题：");
    for (i = 1; i <= 5; i++)
    {
        if (i == 3)
        {
            continue;
        }
        printf("%d", i);
    }
    n = 0;
    for (i = 1; i <= 3; i++)
    {
        for (j = 1; j <= 4; j++)
        {
            n++;
        }
    }
    printf("\n第10题：%d 个\n", n);
    return 0;
}
