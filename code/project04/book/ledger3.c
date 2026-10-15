/* 程序名：ledger3.c
   功能：每个阻值后面紧跟状态字母（如 4.7N），输出电阻实训台账 */
#include <stdio.h>

int main(void)
{
    float r1, r2, r3, r4, r5;          // 5 个电阻的阻值（kΩ）
    char s1, s2, s3, s4, s5;           // 状态：Y 完好，N 损坏

    /* 第一步：输入阻值和状态 */
    printf("请输入 5 个电阻的阻值和状态（如 4.7N，用空格隔开）：\n");
    scanf("%f", &r1);                  // %f 读到字母 Y 或 N 前停下
    s1 = getchar();                    // 紧接着读入状态字母
    scanf("%f", &r2);                  // %f 会自动跳过前面的空格
    s2 = getchar();
    scanf("%f", &r3);
    s3 = getchar();
    scanf("%f", &r4);
    s4 = getchar();
    scanf("%f", &r5);
    s5 = getchar();

    /* 第二步：处理（本任务不需要处理） */

    /* 第三步：输出台账 */
    printf("--------- 电阻实训台账 ---------\n");
    printf("序号        阻值    状态\n");
    printf("%4d%12.2f     ", 1, r1);
    putchar(s1);
    putchar('\n');
    printf("%4d%12.2f     ", 2, r2);
    putchar(s2);
    putchar('\n');
    printf("%4d%12.2f     ", 3, r3);
    putchar(s3);
    putchar('\n');
    printf("%4d%12.2f     ", 4, r4);
    putchar(s4);
    putchar('\n');
    printf("%4d%12.2f     ", 5, r5);
    putchar(s5);
    putchar('\n');
    printf("--------------------------------\n");
    return 0;
}
