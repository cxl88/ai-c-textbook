#include <stdio.h>

int main(void)
{
    unsigned char volt = 380;           // 按 AI 的建议：电压用 unsigned char 保存
    printf("供电电压：%d V\n", volt);
    return 0;
}
