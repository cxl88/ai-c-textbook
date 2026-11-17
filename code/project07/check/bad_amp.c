/* 程序名：bad_amp.c
   功能：错误示范：用 %s 读字符串时在数组名前加 &（只编译、不运行） */
#include <stdio.h>

int main(void)
{
    char name[20];

    scanf("%s", &name);
    printf("%s\n", name);
    return 0;
}
