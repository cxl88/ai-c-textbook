/* 程序名：cp_volt38.c
   功能：核对任务二测试数据第 2、3 组（与 volt38.c 相同） */
#include <stdio.h>

int main(void)
{
    float v[3][8];                     // 3 轮 × 8 路测点电压（V）
    int i, j;                          // 行下标、列下标

    for (i = 0; i < 3; i++)            // 录入：逐轮
    {
        printf("第%d轮V1～V8：", i + 1);
        for (j = 0; j < 8; j++)        // 逐个测点
        {
            scanf("%f", &v[i][j]);
        }
    }
    printf("轮次     V1    V2    V3    V4    V5    V6    V7    V8\n");
    for (i = 0; i < 3; i++)            // 显示：逐轮
    {
        printf("第%d轮", i + 1);
        for (j = 0; j < 8; j++)        // 逐个测点
        {
            printf("%6.2f", v[i][j]);
        }
        printf("\n");
    }
    return 0;
}
