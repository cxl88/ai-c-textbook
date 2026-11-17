/* 程序名：max34.c
   功能：找出 3 行 4 列整数中的最大数及其位置（任务二 技能训练 3） */
#include <stdio.h>

int main(void)
{
    int a[3][4];
    int i, j, r = 0, c = 0;            // 最大数的行下标、列下标

    for (i = 0; i < 3; i++)
    {
        printf("请输入第%d行的4个整数：", i + 1);
        for (j = 0; j < 4; j++)
        {
            scanf("%d", &a[i][j]);
        }
    }
    for (i = 0; i < 3; i++)
    {
        for (j = 0; j < 4; j++)
        {
            if (a[i][j] > a[r][c])
            {
                r = i;
                c = j;
            }
        }
    }
    printf("最大的数是%d，在第%d行第%d列\n", a[r][c], r + 1, c + 1);
    return 0;
}
