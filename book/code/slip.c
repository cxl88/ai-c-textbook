/* 程序名：slip.c
   功能：输出新生报到凭条（资料为虚构） */
#include <stdio.h>

int main(void)
{
    int room = 302;                  // 宿舍房间号
    int bed = 2;                     // 床位号
    double money = 100.0;            // 校园卡初始余额，单位：元

    printf("------ 新生报到凭条 ------\n");
    printf("姓名：%s\n", "林小禾");
    printf("宿舍：6 号楼 %d 室 %d 号床\n", room, bed);
    printf("校园卡余额：%.2f 元\n", money);
    printf("报到时间：%s\n", "9月1日 9:30");
    printf("--------------------------\n");
    return 0;
}
