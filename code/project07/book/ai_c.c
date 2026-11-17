/* 程序名：ai_c.c
   功能：AI 给出的办法③：用结构体把编号和电压放在一起 */
#include <stdio.h>

struct point                           // 结构体：一个测点的编号和电压
{
    int no;
    float v;
};

int main(void)
{
    struct point p[8], t;
    int i, j;

    printf("请输入V1～V8的电压：");
    for (i = 0; i < 8; i++)
    {
        scanf("%f", &p[i].v);
        p[i].no = i + 1;
    }
    for (i = 0; i < 7; i++)
    {
        for (j = 0; j < 7 - i; j++)
        {
            if (p[j].v > p[j + 1].v)
            {
                t = p[j];              // 编号和电压整体交换
                p[j] = p[j + 1];
                p[j + 1] = t;
            }
        }
    }
    printf("从低到高：\n");
    for (i = 0; i < 8; i++)
    {
        printf("V%d  %5.2f\n", p[i].no, p[i].v);
    }
    return 0;
}
