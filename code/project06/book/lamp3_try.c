/* 程序名：lamp3_try.c
   功能：任务三 先试一试：在 lamp2.c 中只加上 break 和 continue */
#include <stdio.h>

int main(void)
{
    int code;                          // 状态码
    int row, col;                      // 第几行、第几列

    for (row = 1; row <= 3; row++)
    {
        printf("请输入第%d行4盏灯的状态码（用空格隔开）：", row);
        for (col = 1; col <= 4; col++)
        {
            scanf("%d", &code);
            if (code == 0)             // 短路不亮：终止巡检
            {
                printf("第%d行第%d列，状态：短路不亮\n", row, col);
                break;
            }
            if (code == 2)             // 闪烁异常：跳过本灯后续处理
            {
                printf("第%d行第%d列，状态：闪烁异常\n", row, col);
                continue;
            }
            // 排除了 0 和 2，状态码就是 1
            printf("第%d行第%d列，状态：正常点亮\n", row, col);
        }
    }
    printf("灯阵全部巡检完毕！\n");
    return 0;
}
