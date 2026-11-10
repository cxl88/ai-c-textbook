#include <stdio.h>

int main(void)
{
    float r = 4700;
    double big = 123456789.0;

    printf("%e\n", r);
    printf("%.2e\n", big);
    printf("%f\n", big);
    printf("%lf\n", 3.5);
    printf("%5.2f|%2d|\n", 123.456, 12345);
    return 0;
}
