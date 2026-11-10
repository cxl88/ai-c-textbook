/* 程序名：assign.c
   功能：观察赋值语句执行后变量值的变化 */
#include <stdio.h>

int main(void)
{
    int score, bonus, a, b, yuan;
    float money;

    score = 80;                // ① 把 80 存入 score
    bonus = 5;                 // ② 把 5 存入 bonus
    score = score + bonus;     // ③ 取出 score 的值加 5，再存回 score
    printf("③ score = %d\n", score);
    score += 10;               // ④ 即 score = score + 10;
    printf("④ score = %d\n", score);
    score -= bonus * 2;        // ⑤ 即 score = score - (bonus * 2);
    printf("⑤ score = %d\n", score);
    a = b = 6;                 // ⑥ 先执行 b = 6，再把 6 赋给 a
    printf("⑥ a = %d，b = %d\n", a, b);
    money = 12.8;              // ⑦ 把 12.8 存入 money
    yuan = money;              // ⑧ 赋给 int 型变量，小数部分被舍去
    printf("⑧ money = %.1f，yuan = %d\n", money, yuan);
    return 0;
}
