/* 程序名：profile8.c（参考答案：离开 AI 再做）
   功能：为另一位同学输出 8 项信息的档案卡片（资料为虚构） */
#include <stdio.h>

int main(void)
{
    int age = 19;                              // 年龄：整数，用 int 型变量保存
    double height = 1.7;                       // 身高：小数，用 double 型变量保存

    printf("==============================\n");
    printf("   校园AI迎新系统 · 新生档案\n");
    printf("==============================\n");
    printf("姓名：%s\n", "陈一鸣");
    printf("学号：%s\n", "2026150307");
    printf("性别：%s\n", "男");
    printf("专业：%s\n", "物联网应用技术");
    printf("年龄：%d 岁\n", age);
    printf("身高：%.2f 米\n", height);
    printf("籍贯：%s\n", "江苏苏州");
    printf("爱好：%s\n", "篮球");
    printf("------------------------------\n");
    printf("祝你新学期学有所成！\n");
    printf("==============================\n");
    return 0;
}
