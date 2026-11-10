#include <stdio.h>

int main(void)
{
    float r;
    char s;

    scanf("%f", &r);
    fflush(stdin);
    s = getchar();
    printf("%c\n", s);
    return 0;
}
