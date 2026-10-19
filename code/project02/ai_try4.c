#include <stdio.h>

int main(void)
{
    int seats = 48, people = 36;        // 总座位数、在室人数
    double rate;                        // 座位利用率（%）

    rate = people / seats * 100.0;      // AI 的建议④
    printf("座位利用率：%.1f%%\n", rate);
    return 0;
}
