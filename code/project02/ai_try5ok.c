#include <stdio.h>

int main(void)
{
    int seats = 48, people = 35;        // 换一组数据：在室 35 人
    double rate;                        // 座位利用率（%）

    rate = (double)people / seats * 100;
    printf("座位利用率：%.1f%%\n", rate);
    return 0;
}
