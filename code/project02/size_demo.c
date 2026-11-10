#include <stdio.h>

int main(void)
{
    printf("short     占 %d 字节\n", (int)sizeof(short));
    printf("int       占 %d 字节\n", (int)sizeof(int));
    printf("long      占 %d 字节\n", (int)sizeof(long));
    printf("long long 占 %d 字节\n", (int)sizeof(long long));
    return 0;
}
