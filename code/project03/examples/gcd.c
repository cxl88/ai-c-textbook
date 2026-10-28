/* 算法举例（3）的程序（选看）：按 S1～S4 用辗转相除法求最大公约数 */
#include <stdio.h>

int main(void)
{
    int m, n, r;

    printf("请输入两个正整数：");
    scanf("%d%d", &m, &n);              // S1：输入两个正整数 ⇒ m、n
    r = m % n;                          // S2：m 除以 n 的余数 ⇒ r
    while (r != 0)                      // S3：余数不为 0 就继续
    {
        m = n;                          // S4：n ⇒ m
        n = r;                          //     r ⇒ n
        r = m % n;                      //     回到 S2，再求余数
    }
    printf("最大公约数是 %d\n", n);     // S3：余数为 0，输出 n
    return 0;
}
