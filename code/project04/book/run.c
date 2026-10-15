/* 程序名：run.c
   功能：输入跑步距离和用时，计算平均配速（顺序结构） */
#include <stdio.h>

int main(void)
{
    float km, minutes, pace;           // 距离、用时、配速

    printf("跑步距离（千米）：");                // ① 提示输入距离
    scanf("%f", &km);                            // ② 输入距离
    printf("用时（分钟）：");                    // ③ 提示输入用时
    scanf("%f", &minutes);                       // ④ 输入用时
    pace = minutes / km;                         // ⑤ 计算配速
    printf("平均配速：%.2f 分钟/千米\n", pace);  // ⑥ 输出结果
    return 0;
}
