/* 课堂练习（例4-14 先输入座位号、再输入组别）验证 */
#include <stdio.h>

int main(void)
{
    char group, g2;
    int seat;

    printf("座位号：");
    scanf("%d", &seat);
    printf("组别（A～F）：");
    getchar();                         // 先读走座位号后面的回车符
    group = getchar();
    printf("组别：%c，座位：%d 号\n", group, seat);
    printf("再输入一次组别：");
    scanf(" %c", &g2);                 // 另一种写法
    printf("组别：%c\n", g2);
    return 0;
}
