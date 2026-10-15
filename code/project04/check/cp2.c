#include <stdio.h>

int main(void)
{
    int a = 1, b = 2;

    printf("%4d|%-4d|\n", 12, 12);
    printf("%.2f\n", 3.14159);
    printf("%6.1f\n", 3.14159);
    printf("完成率：%d%%\n", 95);
    printf("%c%c\n", 'O', 'K');
    printf("%d\n", 'A');
    printf("%d %d\n", a, b);
    return 0;
}
