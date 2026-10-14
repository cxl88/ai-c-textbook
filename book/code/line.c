#include <stdio.h>                           // 包含标准输入输出头文件

void show_line(void)                         // 定义子函数 show_line
{                                            // 子函数的函数体开始
    printf("==========================\n");  // 输出一条分隔线
}                                            // 子函数的函数体结束

int main(void)                               // 主函数：程序从这里开始执行
{                                            // 主函数的函数体开始
    show_line();                             // 调用子函数，输出分隔线
    printf("      校园AI迎新系统\n");          // 输出系统名称
    show_line();                             // 再次调用子函数
    return 0;                                // 结束程序，向系统返回 0
}                                            // 主函数的函数体结束
