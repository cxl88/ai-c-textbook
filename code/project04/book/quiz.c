/* 程序名：quiz.c
   功能：输入题号和答案字母，输出答题记录 */
#include <stdio.h>

int main(void)
{
    int no;                            // 题号
    char ans;                          // 答案：A～D

    printf("题号：");
    scanf("%d", &no);
    getchar();                         // 读走题号后面的回车符
    printf("答案（A～D）：");
    ans = getchar();
    printf("第 %d 题：", no);
    putchar(ans);
    putchar('\n');
    return 0;
}
