/* 程序名：nest_ok.c
   功能：离开 AI 再做 ③参考答案：正确的嵌套写法 */
#include <stdio.h>

int main(void)
{
    float v;                           // 测得的电压（V）

    printf("请输入测得的电压（V）：");
    scanf("%f", &v);
    if (v >= 15)
    {
        if (v <= 21)
        {
            printf("电压正常，组件稳定运行！\n");
        }
        else
        {
            printf("请注意过压！\n");
            if (v <= 24)
            {
                printf("及时核查组件与线路！\n");
            }
            else
            {
                printf("紧急告警，立即停机保护！\n");
            }
        }
    }
    else
    {
        printf("欠压，请检查光伏组件！\n");
    }
    return 0;
}
