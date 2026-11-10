#include <stdio.h>

int main(void)
{
    int people = 38;            // 在室人数
    int size = 4;               // 每组人数
    int groups, left;           // 组数、剩下的人数

    groups = people / size;     // ①
    left = people % size;       // ②
    printf("每组 %d 人，可分 %d 组，余 %d 人\n", size, groups, left);
    people++;                   // ③ 又来了 1 人
    printf("又来 1 人后，在室 %d 人\n", people);
    return 0;
}
