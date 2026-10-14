/* 程序名：zone.c（参考答案）
   功能：输入楼层区字母，输出它的大写形式和区号 */
#include <stdio.h>

int main(void)
{
    char zone;                          // 楼层区字母（a～f）
    char upper;                         // 大写形式
    int no;                             // 区号：a 是 1，b 是 2……

    printf("请输入楼层区字母（a～f）：");
    /* 检查 1：是否读入了一个字符 */
    if (scanf("%c", &zone) != 1)
    {
        printf("没有读到字母，程序结束。\n");
        return 1;
    }
    /* 检查 2：是否是 a～f 中的字母 */
    if (zone < 'a' || zone > 'f')
    {
        printf("输入的不是 a～f 中的字母，程序结束。\n");
        return 1;
    }

    upper = zone - 32;                  // 小写字母转为大写字母
    no = zone - 'a' + 1;                // 与 'a' 相差几，再加 1

    printf("大写形式：%c\n", upper);
    printf("区号：第 %d 区\n", no);
    return 0;
}
