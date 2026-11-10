#include <stdio.h>

int main(void)
{
    int people = 36;            // 在室人数
    int n;

    people++;                   // 进来 1 人：相当于 people = people + 1
    printf("进来 1 人后：people = %d\n", people);
    people--;                   // 离开 1 人：相当于 people = people - 1
    printf("离开 1 人后：people = %d\n", people);

    n = people++;               // 后置：先赋值给 n，people 再加 1
    printf("n = people++ 后：n = %d，people = %d\n", n, people);
    n = ++people;               // 前置：people 先加 1，再赋值给 n
    printf("n = ++people 后：n = %d，people = %d\n", n, people);
    return 0;
}
