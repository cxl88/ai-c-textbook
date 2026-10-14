#include <stdio.h>

int main(void)
{
    printf("整数：%d\n", 18);              // %d：输出十进制整数
    printf("小数：%f\n", 1.68);            // %f：输出小数，默认 6 位小数
    printf("小数：%.2f\n", 1.68);          // %.2f：保留 2 位小数
    printf("字符：%c\n", 'A');             // %c：输出一个字符
    printf("字符串：%s\n", "林小禾");        // %s：输出一个字符串
    printf("报到进度：100%%\n");            // %%：输出一个百分号
    printf("%s 今年 %d 岁，身高 %.2f 米。\n", "小禾", 18, 1.68);
    return 0;
}
