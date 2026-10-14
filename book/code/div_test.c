#include <stdio.h>

int main(void)
{
    int people = 36;                                // 在室人数
    int seats = 48;                                 // 总座位数
    double a = people / seats * 100.0;              // A：先整数除法
    double b = (double)(people / seats) * 100.0;    // B：除完再转换
    double c = (double)people / seats * 100.0;      // C：先转换再除

    printf("写法 A：%.1f%%\n", a);
    printf("写法 B：%.1f%%\n", b);
    printf("写法 C：%.1f%%\n", c);
    return 0;
}
