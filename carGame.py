import pygame
from pygame.locals import *
import sys
import time
import random

WINDOW_WIDTH = 350
WINDOW_HEIGHT = 768

# 期望的FPS值
DEFAULT_FPS = 60
# 每次循环的耗时时间
DEFAULT_DELAY = 1.0 / DEFAULT_FPS - 0.002
i = 0
enemies = []
# 积分
score = 0

def collide(r1, r2):
    """
    判断两个矩形是否碰撞
    :param r1: 矩形1
    :param r2: 矩形2
    :return: true 表示碰撞 false表示没有碰撞
    """
    # 如果r2 在 r1的左边，肯定不会碰撞
    if r1.x > r2.x + r2.width:
        return False
    # 如果r2 在 r1的右边，肯定不会碰撞
    if r1.x + r1.width < r2.x:
        return False
    # 如果r2 在 r1的上边，肯定不会碰撞
    if r1.y > r2.y + r2.height:
        return False
    # 如果r2 在 r1的下边，肯定不会碰撞
    if r1.y + r1.height < r2.y:
        return False
    return True


class Bomb:
    def __init__(self, window,  x, y):
        self.window = window
        self.images = []
        for i in range(1, 14):
            self.images.append(pygame.image.load("img/image {}.png".format(i)))

        self.index = 0
        self.img = self.images[self.index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x - self.width / 2
        self.y = y - self.height / 2

        self.is_destroyed = False

        sound = pygame.mixer.Sound("snd/bomb.wav")
        sound.play()

    def display(self):
        if self.index >= len(self.images):
            self.is_destroyed = True
            return

        self.img = self.images[self.index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.window.blit(self.img, (self.x, self.y))

        self.index += 1


class EnemyPlane:
    def __init__(self, window):
        # 窗体对象
        self.window = window
        self.localtionInit()

    def localtionInit(self):
        self.locationX()
        location_y = [-self.height, -self.height * 5, -self.height * 8]
        global i
        if i >= len(location_y):
            i = 0
        self.y = location_y[i]
        i += 1
    def locationX(self):
        # 图像
        self.img = pygame.image.load("img/monster.gif")
        # 宽和高
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        # 位置
        left = WINDOW_WIDTH/4 - self.width / 2
        right = WINDOW_WIDTH/4 * 3 - self.width/2
        location_x = [left, right]
        self.x = location_x[random.randint(0, len(location_x) - 1)]

    def move(self):
        self.y += 15
        # 飞越界了
        if self.y > WINDOW_HEIGHT:
            global score
            score += 1
            for enemie in enemies:
                if enemie != self:
                    if ((self.y - WINDOW_HEIGHT) + self.height * 3) > enemie.y:
                        self.y = WINDOW_HEIGHT
                    else:
                        self.y = - self.height*2
                        self.reset()



    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def reset(self):
        self.locationX()






class PlayerPlane:
    # 属性
    # 属性初始化的问题
    # 1. 构造内部初始: 自己确定自己处理
    # 2. 外部传入: 自己不确定，外部设置

    def __init__(self, window):
        # 窗体对象
        self.window = window
        # 图像
        self.img = pygame.image.load("img/car3.png")
        # 宽和高
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        # 位置
        self.x = WINDOW_WIDTH/4 - self.width / 2
        self.y = WINDOW_HEIGHT - self.height - 150
        # self._offset = 5
        # 子弹的列表
        self.bullets = []

        # 子弹发射的时间
        self.fire_time = 0
        self.fire_delay = 0.2

    def display(self):
        # 飞机的显示
        self.window.blit(self.img, (self.x, self.y))


    # 函数
    def move_left(self):
        self.x = WINDOW_WIDTH/4 - self.width / 2
        if self.x < -self.width / 2:
            self.x = -self.width / 2

    def move_right(self):
        self.x = WINDOW_WIDTH/4 * 3 - self.width/2
        if self.x > WINDOW_WIDTH - self.width / 2:
            self.x = WINDOW_WIDTH - self.width / 2




if __name__ == '__main__':
    # 初始化
    pygame.init()

    # 设置窗体的大小
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # 设置窗体的title
    pygame.display.set_caption("避障比赛")
    # 设置窗体图标
    pygame.display.set_icon(pygame.image.load("img/monster.gif"))

    # 真实的FPS
    fps = 0

    # 加载字体
    font = pygame.font.Font("font/happy.ttf", 24)
    font_finish = pygame.font.Font("font/happy.ttf", 48)
    finish_text = font_finish.render("游戏结束", True, (0xff, 0, 0))
    ft_width = finish_text.get_width()
    ft_height = finish_text.get_height()
    ft_x = (WINDOW_WIDTH - ft_width) / 2
    ft_y = (WINDOW_HEIGHT - ft_height) / 2 - 50

    # 加载我方的飞机
    player = PlayerPlane(window)

    # 加载敌方飞机
    #enemies = []
    #global enemies
    for i in range(3):
        enemies.append(EnemyPlane(window))

    # 爆炸物
    bombs = []

    # 背景音
    pygame.mixer_music.load("snd/bg2.ogg")
    pygame.mixer_music.play(-1)

    # 游戏结束的标记
    is_over = False

    while True:
        # 开始时间
        start = time.time()

        ########## 图像渲染 #########
        # 背景

        window.fill((0, 0, 0))

        surface = pygame.Surface((3, WINDOW_HEIGHT))
        surface.fill((0xff, 0, 0))

        window.blit(surface, (0, 0))
        window.blit(surface, (WINDOW_WIDTH/2 - 1.5, 0))
        window.blit(surface, (WINDOW_WIDTH - 3, 0))

        # 渲染文本 0x33, 0xCC, 0x33 (0xff, 0xff, 0xff)
        fps_text = font.render("FPS: %d" % fps, True, (0x33, 0xCC, 0x33))
        # 显示fps文本
        window.blit(fps_text, (WINDOW_WIDTH-105, 10))
        # 显示积分
        score_text = font.render("积分: %d" % score, True, (0x33, 0xCC, 0x33))
        # 显示积分文本
        window.blit(score_text, (10, 10))

        if is_over:
            window.blit(finish_text, (ft_x, ft_y))

        if not is_over:
            # 显示我方的飞机
            player.display()

            # 显示敌方飞机
            for enemy in enemies:
                enemy.display()
                enemy.move()

            # 判断我方飞机和敌方飞机是否发生碰撞
            # 1. 敌方飞机矩形
            # 2. 我方飞机矩形
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if collide(player_rect, enemy_rect):
                    # 我方飞机阵亡
                    # 显示爆炸物
                    bombs.append(Bomb(window, player.x + player.width / 2, player.y + player.height / 2))

                    # 游戏要暂停
                    is_over = True

        for bomb in bombs:
            if bomb.is_destroyed:
                bombs.remove(bomb)
            bomb.display()

        # 刷新图像
        pygame.display.flip()

        ######### 事件捕获 ##########
        events = pygame.event.get()
        for event in events:
            # 窗体关闭事件
            if event.type == QUIT:
                # 窗体关闭
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pygame.mixer_music.play(-1)
                if event.key == K_l:
                    pygame.mixer_music.stop()
                if event.key == K_a:
                    player.move_left()
                if event.key == K_d:
                    player.move_right()
                if event.key == K_RETURN and is_over:
                    # 重置状态
                    for enemy in enemies:
                        enemy.localtionInit()
                    score = 0
                    is_over = False




        # 结束时间
        end = time.time()
        # 逻辑耗时
        cost = end - start

        if cost < DEFAULT_DELAY:
            sleep = DEFAULT_DELAY - cost
        else:
            sleep = 0

        # 睡眠
        time.sleep(sleep)

        end = time.time()

        fps = 1.0 / (end - start)
