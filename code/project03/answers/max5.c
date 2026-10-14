/* AI 升华“离开 AI 再做”参考：测量 5 次，输出最大读数 */
#include <stdio.h>

int main(void)
{
    int i;
    float r, max;

    printf("第1次测量值（Ω）：");
    scanf("%f", &max);                // 第 1 个读数先当作最大值
    i = 2;
    while (i <= 5)
    {
        printf("第%d次测量值（Ω）：", i);
        scanf("%f", &r);
        if (r > max)                  // 比目前的最大值还大，就记下来
        {
            max = r;
        }
        i = i + 1;
    }
    printf("最大读数：%.1f Ω\n", max);
    return 0;
}
