#include <stdio.h>

int main(void)
{
    char secret;                        // 收到的加密报文
    char code;                          // 还原出的告警字母

    printf("请输入收到的加密报文（H～O）：");
    secret = getchar();
    if (secret < 'H' || secret > 'O')   // 检查：是否是 H～O 中的字母
    {
        printf("收到的不是 H～O 中的报文，程序结束。\n");
        return 1;
    }
    code = secret - 1 + 32;             // 先减 1 还原大写字母，再加 32 转为小写
    printf("还原出的告警字母：%c\n", code);
    return 0;
}
