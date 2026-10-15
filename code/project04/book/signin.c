/* 程序名：signin.c
   功能：输入组别、座位号和签到时间，输出实训签到条 */
#include <stdio.h>

int main(void)
{
    char group;                        // 组别：A～F
    int seat, hour, minute;            // 座位号、签到时间

    printf("组别（A～F）：");
    group = getchar();
    printf("座位号：");
    scanf("%d", &seat);                // %d 会自动跳过前面留下的回车符
    printf("签到时间（时:分）：");
    scanf("%d:%d", &hour, &minute);    // 冒号要原样输入
    printf("====== 实训签到条 ======\n");
    printf("组别：");
    putchar(group);
    putchar('\n');
    printf("座位：%d 号\n", seat);
    printf("时间：%02d:%02d\n", hour, minute);
    printf("========================\n");
    return 0;
}
