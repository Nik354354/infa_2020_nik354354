from math import sin, cos, atan2, pi
from random import choice, randint as rnd, random

import pygame

# displaying the true size of the window, Windows only
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1700
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
R_MAX = 100


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=HEIGHT-150):
        """ Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.cor = [x, y]
        self.r = 10
        self.v = [0, 0]
        self.color = choice(GAME_COLORS)
        self.live = 2
        self.timer = 10

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.cor[0] и self.cor[1] с учетом скоростей self.v[0] и self.v[1], силы гравитации, действующей на мяч,
        и стен по краям окна.
        """
        self.v[1] += 0.5
        for j in range(2):
            if self.live <= 0:
                self.cor[j] += self.v[j]
                if self.cor[j] + self.v[j] > SIZE[j] - self.r or self.cor[j] + self.v[j] < self.r:
                    self.timer -= 1
            elif self.cor[j] + self.v[j] > SIZE[j] - self.r:
                self.v[j] = -self.v[j]
                self.cor[j] += self.v[j] + 2*(SIZE[j] - self.r - self.cor[j])
                self.live -= 1
            elif self.cor[j] + self.v[j] < self.r:
                self.v[j] = -self.v[j]
                self.cor[j] += self.v[j] + 2*(self.r - self.cor[j])
                self.live -= 1
            else:
                self.cor[j] += self.v[j]

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.cor[0], self.cor[1]),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.center[1] + obj.R * sin(obj.alpha)-self.cor[1]) ** 2 + (obj.center[0] + obj.R * cos(obj.alpha)-self.cor[0]) ** 2 <= (obj.r + self.r) ** 2:
            self.live = False
            return True
        else:
            return False

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча v[0] и v[1] зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = atan2((event.pos[1]-new_ball.cor[1]), (event.pos[0]-new_ball.cor[0]))
        new_ball.v[0] = self.f2_power * cos(self.an)
        new_ball.v[1] = self.f2_power * sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = atan2((event.pos[1]-HEIGHT+150), (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen, self.color, (20, HEIGHT-150),
                        (2 * self.f2_power * cos(self.an) + 30,
                         2 * self.f2_power * sin(self.an) + HEIGHT-150), 20)
    
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 40:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:

    def __init__(self):
        self.screen = screen
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        r = self.r = rnd(6, 50)
        color = self.color = WHITE
        center = self.center = (rnd(150+R_MAX, WIDTH-R_MAX-50), rnd(50+R_MAX, HEIGHT-R_MAX-50))
        R = self.R = rnd(0, R_MAX)
        alpha = self.alpha = 2 * random() * pi

    def move(self):
        self.alpha += 1 / (self.R + 1)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.center[0] + self.R * cos(self.alpha), self.center[1] + self.R * sin(self.alpha)),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.center[0] + self.R * cos(self.alpha), self.center[1] + self.R * sin(self.alpha)),
            self.r,
            2
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 60)
bullet = 0
balls = []
score = 0

clock = pygame.time.Clock()
gun = Gun(screen)
targets = [Target() for i in range(2)]
finished = False

while not finished:
    screen.fill(BLACK)
    gun.draw()
    for t in targets:
        t.draw()
        t.move()
    for b in balls:
        b.draw()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    
    for i in range(len(balls)-1, -1, -1):
        if balls[i].timer <= 0:
            balls.pop(i)
        else:
            balls[i].move()
            for t in targets:
                if balls[i].hittest(t) and t.live:
                    t.live = 0
                    t.new_target()
                    score += 1
    gun.power_up()
    text_score = font.render('Score: ' + str(score), True, [255, 255, 255])
    screen.blit(text_score, (10, 10))
    pygame.display.flip()

pygame.quit()
