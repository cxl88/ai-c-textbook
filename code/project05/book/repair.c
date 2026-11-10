/* 程序名：repair.c
   功能：实训室设备报修菜单（switch 语句） */
#include <stdio.h>

int main(void)
{
    int code;                          // 设备代码

    printf("1-计算机  2-投影仪  3-空调  4-其他\n");
    printf("请输入报修设备代码：");
    scanf("%d", &code);
    switch (code)
    {
    case 1:
    case 2:
        printf("请联系信息中心，电话 8001。\n");
        break;
    case 3:
        printf("请联系后勤处，电话 8002。\n");
        break;
    case 4:
        printf("请联系实训管理员，电话 8003。\n");
        break;
    default:
        printf("代码有误，请重新输入。\n");
    }
    return 0;
}
