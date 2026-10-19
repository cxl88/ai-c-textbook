#include <stdio.h>

int main(void)
{
    int seats = 48, people = 35;        // 换一组数据：在室 35 人
    int rate;                           // 座位利用率（%）

    rate = people * 100 / seats;        // AI 的建议⑤
    printf("座位利用率：%d%%\n", rate);
    return 0;
}
