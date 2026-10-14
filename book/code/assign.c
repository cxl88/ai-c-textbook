#include <stdio.h>

int main(void)
{
    int people = 36;                    // 定义并初始化：在室人数为 36
    printf("上课时：%d 人\n", people);
    people = 40;                        // 赋值：用 40 替换原来的 36
    printf("又来 4 人：%d 人\n", people);
    people = people - 2;                // 先算右边的 40-2，再存回 people
    printf("走了 2 人：%d 人\n", people);
    return 0;
}
