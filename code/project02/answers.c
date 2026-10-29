/* 程序名：answers.c
   功能：上机核对项目二课堂练习和实训巩固中表达式题的答案（教师用） */
#include <stdio.h>
#include <string.h>

int main(void)
{
    int n = 5, x = 10, a = 2, i = 5, j;

    printf("017 = %d\n", 017);
    n = n * 2;
    n = n + 3;
    printf("n = %d\n", n);
    printf("'B' = %d  'b' = %d  '5' = %d\n", 'B', 'b', '5');
    printf("'A' + 2 = %d (%c)  '9' - '0' = %d\n", 'A' + 2, 'A' + 2, '9' - '0');
    printf("sizeof(\"0203\") = %d  strlen(\"0203\") = %d\n", (int)sizeof("0203"), (int)strlen("0203"));
    printf("17 / 5 = %d  17 %% 5 = %d  17.0 / 5 = %.1f  -17 / 5 = %d  2 + 7 %% 3 = %d\n",
           17 / 5, 17 % 5, 17.0 / 5, -17 / 5, 2 + 7 % 3);
    printf("-17 %% 5 = %d\n", -17 % 5);
    j = i++;
    printf("j = i++ : i = %d  j = %d\n", i, j);
    j = ++i;
    printf("j = ++i : i = %d  j = %d\n", i, j);
    x += 5;
    x -= 3;
    x *= 2;
    printf("x = %d\n", x);
    a *= 3 + 4;
    printf("a = %d\n", a);
    a = 3;
    a += a * 2;
    printf("a = %d\n", a);
    printf("10 + 6 / 4 * 2 = %d  20 - 6 %% 4 * 3 = %d  (10 + 6) / 4 * 2 = %d\n",
           10 + 6 / 4 * 2, 20 - 6 % 4 * 3, (10 + 6) / 4 * 2);
    printf("(double)7 / 2 = %.1f  (double)(7 / 2) = %.1f\n", (double)7 / 2, (double)(7 / 2));
    printf("0203 = %d  203 = %d\n", 0203, 203);
    n = 9.9;
    printf("int n = 9.9 -> %d\n", n);
    printf("'D' = %d\n", 'D');
    return 0;
}
