#include <stdlib.h>
#define system(x) printf("\f")
int frames_left = 0;
#define main snake_main
#include "../code/snake.c"
#undef main
int main(int c,char**v){ frames_left=atoi(v[1]); return snake_main(); }
