/* 程序名：fold.c
   功能：一张 0.1 毫米厚的纸，对折几次后厚度超过珠穆朗玛峰？ */
#include <stdio.h>

int main(void)
{
    double h = 0.1;                    // 纸的厚度（毫米）
    int n = 0;                         // 对折的次数

    while (h <= 8848860)               // 8848.86 米 = 8848860 毫米
    {
        h = h * 2;                     // 对折一次，厚度翻一番
        n++;
    }
    printf("对折 %d 次，厚度约 %.0f 米\n", n, h / 1000);
    return 0;
}
