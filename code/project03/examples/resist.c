#include <stdio.h>

int main(void)
{
    int i, ok, bad;
    float r;

    ok = 0;                                   // ① 合格个数清零
    bad = 0;                                  //    不合格个数清零
    i = 1;                                    //    从第 1 个电阻开始
    while (i <= 5)                            // ② 循环：逐个检测
    {
        printf("第%d个电阻的阻值（Ω）：", i);
        scanf("%f", &r);
        if (r >= 95 && r <= 105)              // 选择：判断是否合格
        {
            printf("  合格\n");
            ok = ok + 1;
        }
        else
        {
            printf("  不合格，请放入待检盒\n");
            bad = bad + 1;
        }
        i = i + 1;                            // 准备检测下一个
    }
    printf("合格 %d 个\n", ok);               // ③ 输出合格数
    printf("不合格 %d 个\n", bad);            //    和不合格数
    return 0;
}
