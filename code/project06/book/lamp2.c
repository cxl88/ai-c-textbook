/* 程序名：lamp2.c
   功能：巡检 3 行 4 列共 12 盏指示灯（任务二 第二步） */
#include <stdio.h>

int main(void)
{
    int code;                          // 状态码
    int row, col;                      // 第几行、第几列

    for (row = 1; row <= 3; row++)      // 外层循环：逐行巡检
    {
        printf("请输入第%d行4盏灯的状态码（用空格隔开）：", row);
        for (col = 1; col <= 4; col++)  // 内层循环：逐列巡检
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
