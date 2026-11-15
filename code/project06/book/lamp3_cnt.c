/* 程序名：lamp3_cnt.c
   功能：终止巡检时输出提示和已检测的灯数（任务三 技能训练 2） */
#include <stdio.h>

int main(void)
{
    int code;                          // 状态码
    int row, col;                      // 第几行、第几列
    int stop = 0;                      // 是否终止巡检：0 否，1 是
    int count = 0;                     // 已检测的灯数

    for (row = 1; row <= 3; row++)
    {
        printf("请输入第%d行4盏灯的状态码（用空格隔开）：", row);
        for (col = 1; col <= 4; col++)
        {
            scanf("%d", &code);
            count++;
            if (code == 0)             // 短路不亮：终止巡检
            {
                printf("第%d行第%d列，状态：短路不亮\n", row, col);
                stop = 1;              // 记下：要终止巡检
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
        if (stop == 1)                 // 内层循环是因为短路结束的
        {
            break;                     // 跳出外层循环
        }
    }
    if (stop == 0)                     // 没有短路，才算巡检完毕
    {
        printf("灯阵全部巡检完毕！\n");
    }
    else
    {
        printf("发现短路，巡检终止！已检测 %d 盏灯。\n", count);
    }
    return 0;
}
