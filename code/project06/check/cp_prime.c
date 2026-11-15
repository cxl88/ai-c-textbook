/* 程序名：cp_prime.c
   功能：核对例6-12：判断 91 和 97 时各试了几次 */
#include <stdio.h>

int main(void)
{
    int n, i, t;

    for (n = 91; n <= 97; n = n + 6)
    {
        t = 0;
        for (i = 2; i < n; i++)
        {
            t++;
            if (n % i == 0)
            {
                break;
            }
        }
        printf("n = %d：试了 %d 次，结束时 i = %d\n", n, t, i);
    }
    return 0;
}
