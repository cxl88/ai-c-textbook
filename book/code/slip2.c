/* 程序名：slip2.c（参考答案：改一项需求后的报到凭条）
   功能：输出新生报到凭条（资料为虚构） */
#include <stdio.h>

int main(void)
{
    int room = 415;                  // 宿舍房间号
    int bed = 3;                     // 床位号
    double money = 86.5;             // 校园卡余额，单位：元

    printf("------ 新生报到凭条 ------\n");
    printf("姓名：%s\n", "林小禾");
    printf("宿舍：7 号楼 %d 室 %d 号床\n", room, bed);
    printf("校园卡余额：%.1f 元\n", money);
    printf("报到时间：%s\n", "9月1日 9:30");
    printf("--------------------------\n");
    return 0;
}
