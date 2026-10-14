#include <stdio.h>
extern int frames_left;
static void Sleep(int ms){ (void)ms; step_no++; if(--frames_left==0){ printf("%s","");  fflush(stdout); _Exit(0);} }
