/* 程序名：snake.c
   功能：控制台贪吃蛇小游戏（W/A/S/D 控制方向，Q 退出）
   说明：用到 Windows 专用的 conio.h、windows.h，只能在 Windows 下运行；
        学完数组、循环和函数后，可以回头读懂每一行 */
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <windows.h>

#define W 22                    /* 场地宽（含围墙） */
#define H 12                    /* 场地高（含围墙） */

int sx[200], sy[200];           /* 蛇身每一节的坐标，第 0 节是蛇头 */
int len = 3;                    /* 蛇的长度 */
int fx = 15, fy = 6;            /* 食物的位置 */
int score = 0;                  /* 得分 */

/* 判断 (x, y) 是不是蛇身的一部分（从第 from 节开始找） */
int onSnake(int x, int y, int from)
{
    int i;
    for (i = from; i < len; i++)
    {
        if (sx[i] == x && sy[i] == y)
        {
            return 1;
        }
    }
    return 0;
}

/* 画出整个场地：# 围墙，@ 蛇头，o 蛇身，* 食物 */
void draw(void)
{
    int x, y;
    system("cls");
    for (y = 0; y < H; y++)
    {
        for (x = 0; x < W; x++)
        {
            if (x == 0 || x == W - 1 || y == 0 || y == H - 1)
                putchar('#');
            else if (x == sx[0] && y == sy[0])
                putchar('@');
            else if (onSnake(x, y, 1))
                putchar('o');
            else if (x == fx && y == fy)
                putchar('*');
            else
                putchar(' ');
        }
        putchar('\n');
    }
    printf("得分：%d    W/A/S/D 转向，Q 退出\n", score);
}

int main(void)
{
    int dx = 1, dy = 0;         /* 前进方向：向右 */
    int i, tx, ty;
    char ch;

    for (i = 0; i < len; i++)   /* 蛇的初始位置 */
    {
        sx[i] = 5 - i;
        sy[i] = 5;
    }
    draw();
    while (1)
    {
        if (_kbhit())           /* 有按键才读取，没有按键蛇就继续走 */
        {
            ch = _getch();
            if ((ch == 'w' || ch == 'W') && dy == 0) { dx = 0;  dy = -1; }
            if ((ch == 's' || ch == 'S') && dy == 0) { dx = 0;  dy = 1;  }
            if ((ch == 'a' || ch == 'A') && dx == 0) { dx = -1; dy = 0;  }
            if ((ch == 'd' || ch == 'D') && dx == 0) { dx = 1;  dy = 0;  }
            if (ch == 'q' || ch == 'Q') break;
        }
        tx = sx[len - 1];       /* 记下蛇尾，吃到食物时用来变长 */
        ty = sy[len - 1];
        for (i = len - 1; i > 0; i--)   /* 身体每一节移到前一节的位置 */
        {
            sx[i] = sx[i - 1];
            sy[i] = sy[i - 1];
        }
        sx[0] = sx[0] + dx;     /* 蛇头前进一格 */
        sy[0] = sy[0] + dy;
        if (sx[0] == 0 || sx[0] == W - 1 || sy[0] == 0 || sy[0] == H - 1
            || onSnake(sx[0], sy[0], 1))
        {
            break;              /* 撞墙或咬到自己，游戏结束 */
        }
        if (sx[0] == fx && sy[0] == fy) /* 吃到食物：变长、加分、换食物 */
        {
            sx[len] = tx;
            sy[len] = ty;
            len++;
            score = score + 10;
            do
            {
                fx = rand() % (W - 2) + 1;
                fy = rand() % (H - 2) + 1;
            } while (onSnake(fx, fy, 0));
        }
        draw();
        Sleep(200);             /* 停 0.2 秒，控制速度 */
    }
    printf("游戏结束！最终得分：%d\n", score);
    return 0;
}
