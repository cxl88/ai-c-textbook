/* 程序名：eq_str.c
   功能：错误示范：用 == 比较两个字符串 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char s[10];                        // 状态文本

    printf("请输入状态：");
    scanf("%s", s);
    if (s == "正常")                   // 错误：比较的是存放的位置
    {
        printf("用 == 比较：相同\n");
    }
    else
    {
        printf("用 == 比较：不同\n");
    }
    if (strcmp(s, "正常") == 0)        // 正确：比较的是内容
    {
        printf("用 strcmp 比较：相同\n");
    }
    else
    {
        printf("用 strcmp 比较：不同\n");
    }
    return 0;
}
