/* 程序名：mut_state8.c
   功能：课堂验收（任务三）：删去 case 'A' 后面的 break */
#include <stdio.h>

int main(void)
{
    float v[8];                        // 8 路测点电压（V）
    char code[8];                      // 8 路状态码：A、B、C、D
    int i;

    for (i = 0; i < 8; i++)            // 录入
    {
        printf("请输入V%d的电压和状态码：", i + 1);
        scanf("%f %c", &v[i], &code[i]);
    }
    printf("测点   电压（V）  状态码  状态\n");
    for (i = 0; i < 8; i++)            // 对照输出
    {
        printf("  V%d%12.2f    %c     ", i + 1, v[i], code[i]);
        switch (code[i])
        {
        case 'A':
            printf("支路正常\n");
        case 'B':
            printf("支路开路\n");
            break;
        case 'C':
            printf("支路短路\n");
            break;
        case 'D':
            printf("接触不良\n");
            break;
        default:
            printf("状态码有误\n");
        }
    }
    return 0;
}
