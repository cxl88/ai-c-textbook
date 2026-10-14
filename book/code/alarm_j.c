/* 程序名：alarm.c
   功能：输入告警字母，显示加密后的告警报文 */
#include <stdio.h>
#define ROOM 203                          // 实训室编号
#define TYPE 'C'                          // 实训室类型

int main(void)
{
    char code;                            // 告警字母（g～n）
    char upper;                           // 对应的大写字母
    char secret;                          // 加密报文

    printf("请输入告警字母（g～n）：");
    scanf("%c", &code);                   // 输入：从键盘读入一个字符

    upper = code - 32;                    // 处理 1：小写字母转为大写字母
    secret = upper + 1;                   // 处理 2：取相邻的下一个字母

    printf("====== %d 实训室告警上报 ======\n", ROOM);
    printf("实训室类型：%c\n", TYPE);
    printf("告警字母：%c\n", code);
    printf("大写字母：%c\n", upper);
    printf("加密报文：%c\n", secret);
    return 0;
}
