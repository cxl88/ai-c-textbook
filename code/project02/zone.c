/* 程序名：zone.c
   功能：由楼层区号字母求出大写形式和区号 */
#include <stdio.h>

int main(void)
{
    char z = 'c';               // 楼层区号字母（a～f）
    char big;                   // 大写形式
    int no;                     // 第几区

    big = z - 32;
    no = z - 'a' + 1;
    printf("大写形式：%c\n", big);
    printf("区号：第 %d 区\n", no);
    return 0;
}
