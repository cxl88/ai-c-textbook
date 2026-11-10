#include <stdio.h>

int main(void)
{
    char secret;                // 收到的加密报文
    char code;                  // 还原出的告警字母

    secret = 'H';               // 在任务二的基础上完成
    code = secret - 1 + 32;     // 处理过程
    printf("还原出的告警字母：%c\n", code);
    return 0;
}
