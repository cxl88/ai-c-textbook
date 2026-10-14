#include <stdio.h>
#define ROOM 203                        // 符号常量：实训室编号

int main(void)
{
    const int seats = 48;               // 只读变量：总座位数，之后不能再修改

    printf("整型常量：%d\n", 48);
    printf("浮点型常量：%.1f\n", 24.5);
    printf("字符常量：%c\n", 'C');
    printf("字符串常量：%s\n", "6号楼实训室");
    printf("符号常量 ROOM：%d\n", ROOM);
    printf("只读变量 seats：%d\n", seats);
    return 0;
}
