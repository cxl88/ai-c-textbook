#include <stdio.h>

int main(void)
{
    char code = 'k';
    char secret = code - 32 + 1;
    printf("告警字母：%c\n", code);
    printf("加密报文：%c\n", secret);
    return 0;
}
