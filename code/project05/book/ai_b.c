/* 程序名：ai_b.c
   功能：AI 给出的写法②（转成整数后用 switch） */
#include <stdio.h>

int main(void)
{
    float v;

    printf("请输入测得的电压（V）：");
    scanf("%f", &v);
    switch ((int)v)
    {
    case 15 ... 21:
        printf("电压正常，组件稳定运行！\n");
        break;
    case 22 ... 24:
        printf("请注意过压！\n");
        printf("及时核查组件与线路！\n");
        break;
    default:
        if (v < 15)
        {
            printf("欠压，请检查光伏组件！\n");
        }
        else
        {
            printf("请注意过压！\n");
            printf("紧急告警，立即停机保护！\n");
        }
    }
    return 0;
}
