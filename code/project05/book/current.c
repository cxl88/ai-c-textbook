/* 程序名：current.c
   功能：电流读数为负时提醒表笔接反，并取绝对值 */
#include <stdio.h>

int main(void)
{
    float i;                           // 万用表读数（mA）

    printf("万用表读数（mA）：");
    scanf("%f", &i);
    if (i < 0)                         // 读数是负数吗？
    {
        printf("表笔接反了，请交换红、黑表笔！\n");
        i = -i;                        // 取相反数，得到电流大小
    }
    printf("电流大小：%.2f mA\n", i);
    return 0;
}
