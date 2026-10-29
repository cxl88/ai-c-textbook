/* bad_204.c 的参考答案 */
#include <stdio.h>

int main(void)
{
    int seats = 40, people = 30;        // 总座位数、在室人数
    double rate;                        // 座位利用率（%）
    double volt = 221.5, amp = 1.2;     // 工作电压（V）、工作电流（A）
    double power;                       // 功率（W）

    rate = (double)people / seats * 100;
    power = volt * amp;
    printf("座位利用率：%.1f%%\n", rate);
    printf("计算机功率：%.2f W\n", power);
    return 0;
}
