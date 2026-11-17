/* 程序名：name_in.c
   功能：输入姓名，输出问候语（用 %s 输入、输出字符串） */
#include <stdio.h>

int main(void)
{
    char name[20];                     // 最多 9 个汉字或 19 个字母

    printf("请输入你的姓名：");
    scanf("%s", name);                 // 数组名前不加 &
    printf("你好，%s！欢迎来到电工电子实训室。\n", name);
    return 0;
}
