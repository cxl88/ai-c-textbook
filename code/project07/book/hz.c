/* 程序名：hz.c
   功能：字符串在字符数组中的存放（本书环境：一个汉字占 2 个字节） */
#include <stdio.h>

int main(void)
{
    char s1[] = "OK";                  // 省略长度，由字符串确定
    char s2[] = "支路正常";
    char s3[10] = "Hi";                // 其余元素都是 '\0'

    printf("s1：%s，占%d个字节\n", s1, (int)sizeof(s1));
    printf("s2：%s，占%d个字节\n", s2, (int)sizeof(s2));
    printf("s3：%s，占%d个字节\n", s3, (int)sizeof(s3));
    return 0;
}
