/* 程序名：cp_moon.c
   功能：核对趣味小站：0.1 毫米厚的纸对折几次，厚度超过地球到月球的距离（约 38.44 万千米） */
#include <stdio.h>

int main(void)
{
    double h = 0.1;                    // 毫米
    int n = 0;

    while (h <= 384400.0 * 1000 * 1000)  // 384400 千米换算成毫米
    {
        h = h * 2;
        n++;
    }
    printf("对折 %d 次，厚度约 %.0f 千米\n", n, h / 1000 / 1000);
    return 0;
}
