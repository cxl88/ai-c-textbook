/* 程序名：group.c
   功能：实训课分组，求能分成几组、还剩几人 */
#include <stdio.h>

int main(void)
{
    int people = 36;            // 在室人数
    int size = 5;               // 每组人数
    int groups, left;           // 组数、剩下的人数

    groups = people / size;     // 整除：能分成几个完整的组
    left = people % size;       // 求余：分完后还剩几人
    printf("%d 人，每组 %d 人\n", people, size);
    printf("可以分成 %d 组，还剩 %d 人\n", groups, left);
    return 0;
}
