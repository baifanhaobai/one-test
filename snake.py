"""简易终端贪吃蛇（Windows）

运行:  python snake.py
操作:  WASD 或方向键移动，Q 退出
"""

import os
import random
import time

import msvcrt

W, H = 20, 20      # 棋盘宽高（格子数）
SPEED = 0.12       # 每帧间隔（秒），越小越快
DIRS = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}
ARROWS = {'H': 'w', 'P': 's', 'K': 'a', 'M': 'd'}


def clear_screen():
    os.system('')  # 让 Windows 控制台支持下面的 ANSI 转义序列
    print('\033[2J\033[H', end='')


def read_key():
    """非阻塞读键：返回本帧最后一次按下的方向键或 'q'，没按键返回 None。"""
    key = None
    while msvcrt.kbhit():
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):          # 方向键会先发一个前缀字节
            ch = ARROWS.get(msvcrt.getwch(), '')
        ch = ch.lower()
        if ch in DIRS or ch == 'q':
            key = ch
    return key


def spawn_food(snake):
    """在空格子里随机放一个食物；棋盘满了返回 None。"""
    taken = set(snake)
    empty = [(x, y) for y in range(H) for x in range(W) if (x, y) not in taken]
    return random.choice(empty) if empty else None


def draw(snake, food, score):
    body = set(snake)
    out = [f'\033[H 得分: {score}    WASD/方向键移动   Q 退出\033[K',
           '  +' + '-' * (W * 2) + '+\033[K']
    for y in range(H):
        row = []
        for x in range(W):
            if (x, y) == snake[0]:
                row.append('@ ')
            elif (x, y) in body:
                row.append('o ')
            elif (x, y) == food:
                row.append('* ')
            else:
                row.append('  ')
        out.append('  |' + ''.join(row) + '|\033[K')
    out.append('  +' + '-' * (W * 2) + '+\033[K')
    print('\n'.join(out), flush=True)


def play():
    """玩一局，返回 (得分, 结束语)；中途按 Q 退出返回 None。"""
    snake = [(W // 2, H // 2), (W // 2 - 1, H // 2), (W // 2 - 2, H // 2)]
    direction = 'd'
    food = spawn_food(snake)
    score = 0
    clear_screen()

    while True:
        key = read_key()
        if key == 'q':
            return None
        if key in DIRS:                   # key 为 None 时这样写也不会报错
            dx, dy = DIRS[direction]
            kx, ky = DIRS[key]
            if (kx, ky) != (-dx, -dy):    # 不允许直接掉头
                direction = key

        dx, dy = DIRS[direction]
        head = (snake[0][0] + dx, snake[0][1] + dy)
        eating = head == food
        hit_wall = not (0 <= head[0] < W and 0 <= head[1] < H)
        hit_self = head in (snake if eating else snake[:-1])  # 尾巴这帧会让开
        if hit_wall or hit_self:
            return score, '游戏结束'

        snake.insert(0, head)
        if eating:
            score += 10
            food = spawn_food(snake)
        else:
            snake.pop()

        draw(snake, food, score)
        if food is None:
            return score, '棋盘被填满，你赢了！'
        time.sleep(SPEED)


def game_over(score, message):
    clear_screen()
    print(f'{message}  最终得分: {score}')
    print('按 R 再来一局，按其他键退出')
    return msvcrt.getwch().lower() == 'r'


def main():
    while True:
        result = play()
        if result is None:
            clear_screen()
            print('已退出。')
            return
        if not game_over(*result):
            clear_screen()
            print('游戏结束，再见！')
            return


if __name__ == '__main__':
    main()
