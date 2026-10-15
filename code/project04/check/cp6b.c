/* 课堂练习：年龄和性别，写法 B */
#include <stdio.h>

int main(void)
{
    int age;
    char sex;

    scanf("%d", &age);
    scanf(" %c", &sex);                // 写法 B
    printf("age = %d, sex 的 ASCII 码 = %d（%c）\n", age, sex, sex);
    return 0;
}
