/* 程序名：abn_code.c
   功能：只输出状态异常的支路，并统计路数（任务三 技能训练 2） */
#include <stdio.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    char code[8];                      // 8 路状态码：A、B、C、D
    int i, count = 0;                  // 下标、异常的支路数

    for (i = 0; i < 8; i++)
    {
        printf("请输入V%d的电压和状态码：", i + 1);
        scanf("%f %c", &v[i], &code[i]);
    }
    printf("状态异常的支路：\n");
    for (i = 0; i < 8; i++)
    {
        if (code[i] != 'A')
        {
            printf("  V%d%8.2f V  %c\n", i + 1, v[i], code[i]);
            count++;
        }
    }
    printf("共%d路\n", count);
    return 0;
}
