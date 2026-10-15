/* 程序名：resist.c
   功能：逐个检测 5 个标称 100 Ω 的电阻，
         阻值在 95～105 Ω 之间为合格，最后统计合格个数 */
#include <stdio.h>

int main(void)
{
    int i, ok;
    float r;

    ok = 0;                                    // 合格个数，先清零
    i = 1;
    while (i <= 5)                             // 循环：逐个检测
    {
        printf("第%d个电阻的阻值（Ω）：", i);
        scanf("%f", &r);
        if (r >= 95 && r <= 105)               // 选择：判断是否合格
        {
            printf("  合格\n");
            ok = ok + 1;
        }
        else
        {
            printf("  不合格，请放入待检盒\n");
        }
        i = i + 1;
    }
    printf("检测完毕：合格 %d 个，不合格 %d 个\n", ok, 5 - ok);
    return 0;
}
