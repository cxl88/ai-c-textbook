/* 程序名：bad_bound.c
   功能：错误示范：下标越界（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    int i;

    for (i = 1; i <= 8; i++)
    {
        printf("请输入V%d的电压（V）：", i);
        scanf("%f", &v[i]);
    }
    for (i = 1; i <= 8; i++)
    {
        printf("V%d：%.2f\n", i, v[i]);
    }
    return 0;
}
