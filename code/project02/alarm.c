/* 程序名：alarm.c
   功能：显示加密后的告警报文 */
#include <stdio.h>

int main(void)
{
    char code;                  // 告警字母
    char upper;                 // 对应的大写字母
    char secret;                // 加密报文

    code = 'g';                 // 赋值：告警字母 g
    upper = code - 32;          // 处理 1：小写字母转为大写字母
    secret = upper + 1;         // 处理 2：取相邻的下一个字母

    printf("== 教师计算机告警上报 ==\n");
    printf("告警字母：%c\n", code);
    printf("加密报文：%c\n", secret);
    return 0;
}
