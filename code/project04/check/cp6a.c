/* 课堂练习：年龄和性别，写法 A */
#include <stdio.h>

int main(void)
{
    int age;
    char sex;

    scanf("%d", &age);
    sex = getchar();                   // 写法 A
    printf("age = %d, sex 的 ASCII 码 = %d（%c）\n", age, sex, sex);
    return 0;
}
