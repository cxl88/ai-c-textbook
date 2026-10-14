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
    if (scanf("%c", &code) != 1)          // 检查 1：是否读入了一个字符
    {
        printf("没有读到告警字母，程序结束。\n");
        return 1;
    }
    if (code < 'g' || code > 'n')         // 检查 2：是否是 g～n 中的字母
    {
        printf("输入的不是 g～n 中的告警字母，程序结束。\n");
        return 1;
    }

    upper = code - 32;                    // 处理 1：小写字母转为大写字母
    secret = upper + 1;                   // 处理 2：取相邻的下一个字母

    printf("====== %d 实训室告警上报 ======\n", ROOM);
    printf("实训室类型：%c\n", TYPE);
    printf("告警字母：%c\n", code);
    printf("大写字母：%c\n", upper);
    printf("加密报文：%c\n", secret);
    return 0;
}
