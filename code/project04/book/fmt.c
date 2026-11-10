/* 程序名：fmt.c
   功能：用 printf 输出实训室信息卡 */
#include <stdio.h>

int main(void)
{
    int room = 203;                    // 实训室编号
    char type = 'C';                   // 实训室类型
    float area = 86.5;                 // 面积（平方米）
    float rate = 96.8;                 // 设备完好率（%）

    printf("实训室：%d\n", room);             // %d：输出整数
    printf("类型：%c\n", type);               // %c：输出一个字符
    printf("面积：%f 平方米\n", area);        // %f：默认输出 6 位小数
    printf("面积：%.1f 平方米\n", area);      // %.1f：保留 1 位小数
    printf("完好率：%.1f%%\n", rate);         // %%：输出一个 %
    printf("门牌：\"%d-%c\"\n", room, type);  // \"：输出一个双引号
    return 0;
}
