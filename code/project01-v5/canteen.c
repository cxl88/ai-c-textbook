/* 程序名：canteen.c
   功能：食堂点餐小程序（菜品和价格为虚构）
   用到的知识：printf 输出、scanf 输入、数组、选择和循环 */
#include <stdio.h>

int main(void)
{
    char name[4][20] = {"红烧肉盖饭", "番茄炒蛋饭", "牛肉拉面", "绿豆汤"};
    double price[4] = {15.0, 10.0, 13.0, 2.5};
    int choice, num, i;
    double total = 0;

    printf("====== 一食堂点餐 ======\n");
    for (i = 0; i < 4; i++)                      /* 循环输出菜单 */
    {
        printf("%d. %-10s %5.1f 元\n", i + 1, name[i], price[i]);
    }
    printf("0. 结账\n");

    while (1)                                    /* 反复点餐，输入 0 结账 */
    {
        printf("请输入菜品编号：");
        if (scanf("%d", &choice) != 1 || choice == 0)
        {
            break;
        }
        if (choice < 1 || choice > 4)            /* 选择：编号不对就提示 */
        {
            printf("没有这个菜品，请重新输入。\n");
            continue;
        }
        printf("份数：");
        if (scanf("%d", &num) != 1 || num < 1)
        {
            break;
        }
        total = total + price[choice - 1] * num; /* 计算：累计金额 */
        printf("已点 %s × %d，当前合计 %.1f 元\n", name[choice - 1], num, total);
    }
    printf("合计：%.1f 元，请扫码支付，祝用餐愉快！\n", total);
    return 0;
}
