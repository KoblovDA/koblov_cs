import math
from random import choice
from random import randint as rnd
import pygame
import pygame.freetype

FPS = 30

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
WIDTH = 800
HEIGHT = 600
g = 2


class Shot:
    def __init__(self):
        """
        Конструирует выстрел шариком или лазером.
        x и y - центр шарика или начальная точка выстрела лазера - оба совпадают с координатами пушки
        """
        global gun, screen
        self.x = gun.x
        self.y = gun.y
        self.screen = screen


class Ball(Shot):
    def __init__(self):
        """ Конструктор класса ball
        r - радиус шара, vx и vy - скорости по осям, color - цвет, live - параметр жизни
        """

        super(Ball, self).__init__()

        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации и силы сопротивления воздуха, действующих
        на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy = (self.vy - g) * 0.99
        self.vx = 0.98 * self.vx
        self.x += self.vx
        self.y -= self.vy - g / 2
        if self.x > 800 - self.r:
            self.vx = -self.vx * 0.8
            self.x = 800
        if self.x < self.r:
            self.vx = -self.vx * 0.8
            self.x = 0
        if self.y > 500:
            self.vy = - self.vy * 0.8
            self.y = 500

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hit_test(self, obj, num):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
            num: 0 для столкновения с круглой целью и 1 для столкновения с квадратом
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if num == 0:
            return (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= (obj.r + self.r) ** 2
        else:
            return max(abs(obj.x - self.x), abs(obj.y - self.y)) <= obj.r + self.r


class Laser(Shot):
    def __init__(self):
        """
        Инициализация лазера. width - параметр ширины линии, которая должна рисоваться,
        angle - угол, под которым стреляет лазер (зависит от положения мыши в данный момент),
        live - параметр жизни (лазер должен исчезать через некоторое время после применения)
        """
        super(Laser, self).__init__()
        self.width = 5
        self.angle = 1
        self.live = 0

    def draw(self):
        """
        Прорисовка лазера. Рисует его как линию с заданными наклоном, определяемым мышью, уходящей до конца экрана."
        """
        pygame.draw.line(self.screen, RED, (self.x + 60 * math.cos(self.angle), self.y - 60 * math.sin(self.angle)),
                         (self.x + 1000 * math.cos(self.angle), self.y - math.sin(self.angle) * 1000), self.width)

    def move(self, event, gun):
        """
        Движение лазера, учитывающее движение пушки и её поворот
        """
        self.angle = -math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        self.x = gun.x
        self.y = gun.y

    def hit_test(self, obj):
        """
        Проверка на попадание лазера в КРУГЛУЮ цель с помощью формулы расстояния от точки до прямой.
        Квадратные цели лазер не задевает.
        """
        normal = [math.tan(self.angle), 1]
        return abs(((normal[0] * (obj.x - self.x) + normal[1] * (obj.y - self.y)) / (
                normal[0] ** 2 + normal[1] ** 2) ** 0.5)) <= obj.r


class Gun:
    def __init__(self, screen):
        """
        Инициализация пушки. f2_on и f2_power - параметры, отвечающие за то, пытается ли выстрелить в данный момент
        пушка шариком. an - угол поворота пушки, x и y - координаты левой нижней точки пушки.
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450

    def move(self, key):
        """
        Реализовано стандартное движение в соответствии с нажатыми кнопками - WASD
        """
        if key[pygame.K_d]:
            self.x += 5
        if key[pygame.K_a]:
            self.x -= 5
        if key[pygame.K_w]:
            self.y -= 5
        if key[pygame.K_s]:
            self.y += 5

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = -math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = -math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """
        Прорисовка пушки как удлинняющегося прямоугольника в направлении, указанном мышкой. Цвет пушки изменяется
        """
        delta = (50 + self.f2_power)
        pygame.draw.polygon(self.screen, (2 * self.f2_power, 2 * self.f2_power, self.f2_power),
                            ((self.x, self.y), (self.x + delta * math.cos(self.an), self.y - delta * math.sin(self.an)),
                             (self.x + delta * math.cos(self.an) - 10 * math.sin(self.an),
                              self.y - delta * math.sin(self.an) - 10 * math.cos(self.an)),
                             (self.x - 10 * math.sin(self.an),
                              self.y - 10 * math.cos(self.an))))

    def power_up(self):
        """
        Доп функция, связанная с удлиннением пушки
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Enemy:
    def __init__(self):
        """
        Инициализируется класс врагов, появляющихся в случайном месте со случайными скоростями и параметром жизни
        live, необходимым для удаления его при попадании в него.
        """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        self.live = 1

    def move(self):
        """
        Движение врага без учёта гравитации с учётом отражения от стенок
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x > 800 - self.r:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x < self.r:
            self.vx = -self.vx
            self.x = self.r
        if self.y > 500:
            self.vy = - self.vy
            self.y = 500
        if self.y < self.r:
            self.vy = - self.vy
            self.y = self.r


class Target(Enemy):
    def __init__(self):
        """ Инициализация круглого врага со случайными радиусом и цветом """
        super(Target, self).__init__()
        self.r = rnd(10, 50)
        self.color = GAME_COLORS[rnd(0, 5)]

    def draw(self):
        """
        Прорисовка круглого врага
        """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Square(Enemy):
    def __init__(self):
        """Аналогично с круглым"""
        super(Square, self).__init__()
        self.color = BLACK
        self.live = 1
        self.r = rnd(5, 15)

    def jump(self):
        """
        Особенность движения квадратного врага - он может прыгнуть на фиксированное расстояние вниз-вверх или
        вправо-влево (или одновременно в две стороны)
        """
        if 700 - self.r > self.x > 100 + self.r and 100 + self.r < self.y < 500 - self.r:
            if rnd(0, 100) < 25:
                rnd_x = rnd(-1, 1)
                rnd_y = rnd(-1, 1)
                self.x += rnd_x * 70
                self.y += rnd_y * 70

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r))


class Bomb:
    def __init__(self):
        """
        Инициализация бомб, падающих сверху из случайного места с разбросом скоростей
        """
        self.x = rnd(50, 750)
        self.y = -10
        self.vy = rnd(6, 15)
        self.r = rnd(10, 25)
        self.color = BLACK
        self.live = 1

    def move(self):
        """Движение бомбы"""
        self.y += self.vy

    def draw(self):
        """Прорисовка бомбы"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r, 2)

    def hit_test(self, obj):
        """Проверяет, столкнулась ли бомба с объектом (пушкой)"""
        return (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= self.r ** 2


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_FONT = pygame.freetype.Font("arial.ttf", 40)
bullet = 0
score = 0
balls = []
squares = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
laser = Laser()
targets = [Target() for _ in range(5)]
squares = [Square() for _ in range(2)]
bombs = [Bomb() for _ in range(5)]
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for obj in targets:
        obj.draw()
    for obj in squares:
        obj.draw()
    for b in balls:
        if b.vx ** 2 + b.vy ** 2 > 3 or b.y < 485 + b.r:
            b.draw()
    if laser.live > 0:
        laser.draw()
        laser.live -= 1
    text_surface, rect = GAME_FONT.render("Score: " + str(score), BLACK)
    screen.blit(text_surface, (50, 50))
    for obj in bombs:
        obj.draw()
        if obj.hit_test(gun):
            text_surface, rect = GAME_FONT.render("GAME OVER" + str(score), BLACK)
            finished = True

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys:
            gun.move(keys)
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                gun.fire2_start(event)
            elif event.button == 3:
                laser.live = 10

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            laser.move(event, gun)
            gun.targeting(event)
    for b in balls:
        b.move()
        for obj in targets:
            if b.hit_test(obj, 0) and obj.live:
                obj.live = 0
                score += 1
                obj.__init__()
        for obj in squares:
            if b.hit_test(obj, 1) and obj.live:
                obj.live = 0
                score += 5
                obj.__init__()
    for obj in targets:
        if laser.hit_test(obj) and obj.live and laser.live > 0:
            obj.live = 0
            score += 1
            obj.__init__()
        obj.move()

    for obj in squares:
        obj.move()
        obj.jump()
    for obj in bombs:
        if obj.y > 600:
            obj.live = 0
            obj.__init__()
        obj.move()
    gun.power_up()
pygame.quit()
