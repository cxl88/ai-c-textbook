/* 算法举例（2）的程序（选看）：按 S1～S5 判断闰年。if…else 的完整写法在后续项目学习 */
#include <stdio.h>

int main(void)
{
    int year;

    printf("请输入年份：");
    scanf("%d", &year);                     // S1：输入年份 ⇒ year
    if (year % 400 == 0)                    // S2：能被 400 整除吗？
    {
        printf("%d 年是闰年\n", year);
    }
    else if (year % 100 == 0)               // S3：能被 100 整除吗？
    {
        printf("%d 年不是闰年\n", year);
    }
    else if (year % 4 == 0)                 // S4：能被 4 整除吗？
    {
        printf("%d 年是闰年\n", year);
    }
    else
    {
        printf("%d 年不是闰年\n", year);
    }
    return 0;                               // S5：结束
}
