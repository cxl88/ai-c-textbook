/* 程序名：row1.c
   功能：巡检第 1 行的 4 盏指示灯（任务二 第一步） */
#include <stdio.h>

int main(void)
{
    int code;                          // 状态码
    int row = 1;                       // 第几行：本步只巡检第 1 行
    int col;                           // 第几列

    printf("请输入第%d行4盏灯的状态码（用空格隔开）：", row);
    for (col = 1; col <= 4; col++)
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
    return 0;
}
