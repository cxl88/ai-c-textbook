#include <stdio.h>

int main(void)
{
    printf("short     占 %d 字节\n", (int)sizeof(short));
    printf("int       占 %d 字节\n", (int)sizeof(int));
    printf("long      占 %d 字节\n", (int)sizeof(long));
    printf("long long 占 %d 字节\n", (int)sizeof(long long));
    printf("float     占 %d 字节\n", (int)sizeof(float));
    printf("double    占 %d 字节\n", (int)sizeof(double));
    printf("char      占 %d 字节\n", (int)sizeof(char));
    printf("_Bool     占 %d 字节\n", (int)sizeof(_Bool));
    return 0;
}
