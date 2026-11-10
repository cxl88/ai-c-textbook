#include <stdio.h>

int main(void)
{
    float f = 1234567.89f;              // 单精度：约 6～7 位有效数字
    double d = 1234567.89;              // 双精度：约 15～16 位有效数字

    printf("float  保存的值：%f\n", f);  // %f 默认输出 6 位小数
    printf("double 保存的值：%f\n", d);
    printf("保留 2 位小数：%.2f\n", d);
    return 0;
}
