/* 算法举例（1）的程序（选看）：按 S1～S6 求 1+2+3+…+n。
   把第 5 行的 5 改成 1000 或 10000，就能求 1 加到 1000、1 万 */
#include <stdio.h>

#define N 1000                  // 加到几就改成几

int main(void)
{
    int i, sum;

    sum = 0;                            // S1：0 ⇒ sum
    i = 1;                              // S2：1 ⇒ i
    while (i <= N)                      // S5：i ≤ N 就回到 S3，否则执行 S6
    {
        sum = sum + i;                  // S3：sum + i ⇒ sum
        i = i + 1;                      // S4：i + 1 ⇒ i
    }
    printf("1+2+…+%d = %d\n", N, sum);  // S6：输出 sum
    return 0;
}
