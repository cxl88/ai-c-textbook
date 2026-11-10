#include <stdio.h>

int main(void)
{
    int people = 36, seats = 48;                // 在室人数、总座位数

    printf("写法 A：%.1f%%\n", people / seats * 100.0);
    printf("写法 B：%.1f%%\n", (double)(people / seats) * 100);
    printf("写法 C：%.1f%%\n", (double)people / seats * 100);
    return 0;
}
