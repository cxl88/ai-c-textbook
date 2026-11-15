/* 程序名：lamp2_rc.c
   功能：灯阵的行数和列数由键盘输入（任务二 技能训练 2） */
#include <stdio.h>

int main(void)
{
    int code, row, col;                // 状态码、第几行、第几列
    int rows, cols;                    // 灯阵的行数、列数

    printf("请输入灯阵的行数和列数：");
    scanf("%d%d", &rows, &cols);
    for (row = 1; row <= rows; row++)
    {
        printf("请输入第%d行%d盏灯的状态码（用空格隔开）：", row, cols);
        for (col = 1; col <= cols; col++)
        {
            scanf("%d", &code);
            if (code == 1)
            {
                printf("第%d行第%d列，状态：正常点亮\n", row, col);
            }
            else if (code == 2)
            {
                printf("第%d行第%d列，状态：闪烁异常\n", row, col);
            }
            else if (code == 0)
            {
                printf("第%d行第%d列，状态：短路不亮\n", row, col);
            }
        }
    }
    printf("灯阵全部巡检完毕！\n");
    return 0;
}
