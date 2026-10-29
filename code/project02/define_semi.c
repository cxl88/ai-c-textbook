#include <stdio.h>
#define SEATS 48;               // 错误：末尾多了分号

int main(void)
{
    int people = 36;
    int empty = SEATS - people;
    printf("%d\n", empty);
    return 0;
}
