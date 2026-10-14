/* 程序名：alarm_given.c
   功能：先用给定的告警字母测试处理过程（任务二第三步） */
#include <stdio.h>
#define ROOM 203                          // 实训室编号
#define TYPE 'C'                          // 实训室类型

int main(void)
{
    char code;                            // 告警字母（g～n）
    char upper;                           // 对应的大写字母
    char secret;                          // 加密报文

    code = 'g';                           // 先用给定的告警字母测试
    upper = code - 32;                    // 处理 1：小写字母转为大写字母
    secret = upper + 1;                   // 处理 2：取相邻的下一个字母

    printf("加密报文：%c\n", secret);      // 输出：加密报文
    return 0;
}
