/* 程序名：mut_volt3.c
   功能：课堂验收（任务三）：把 v <= 24 改成 v < 24 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    /* 输入 */
    printf("请输入测得的电压（V）：");
    scanf("%f", &v);

    /* 处理和输出 */
    if (v < 15)
    {
        printf("欠压，请检查光伏组件！\n");
    }
    else if (v <= 21)
    {
        printf("电压正常，组件稳定运行！\n");
    }
    else                               // v＞21：过压
    {
        printf("请注意过压！\n");
        if (v < 24)                    // 21＜v≤24：过压预警
        {
            printf("及时核查组件与线路！\n");
        }
        else                           // v＞24：紧急过压
        {
            printf("紧急告警，立即停机保护！\n");
        }
    }
    return 0;
}
