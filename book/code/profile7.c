/* 程序名：profile7.c
   功能：输出包含 7 项信息的个人专属档案卡片（资料为虚构） */
#include <stdio.h>

int main(void)
{
    int age = 18;                              // 年龄：整数，用 int 型变量保存
    double height = 1.68;                      // 身高：小数，用 double 型变量保存

    printf("==============================\n");
    printf("   校园AI迎新系统 · 新生档案\n");
    printf("==============================\n");
    printf("姓名：%s\n", "林小禾");
    printf("学号：%s\n", "2026150218");
    printf("性别：%s\n", "女");
    printf("专业：%s\n", "人工智能技术应用");
    printf("年龄：%d 岁\n", age);
    printf("身高：%.2f 米\n", height);
    printf("籍贯：%s\n", "浙江杭州");
    printf("------------------------------\n");
    printf("祝你新学期学有所成！\n");
    printf("==============================\n");
    return 0;
}
