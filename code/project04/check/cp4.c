#include <stdio.h>

int main(void)
{
    char c, d;

    putchar('A' + 2);
    putchar('\n');
    c = getchar();
    d = getchar();
    printf("c = %c(%d), d = %c(%d)\n", c, c, d, d);
    return 0;
}
