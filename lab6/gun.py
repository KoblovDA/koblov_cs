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
        global gun, screen
        self.x = gun.x
        self.y = gun.y
        self.screen = screen


class Ball(Shot):
    def __init__(self, screen: pygame.Surface, gun):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
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
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
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
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if num == 0:
            return (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= (obj.r + self.r) ** 2
        else:
            return max(abs(obj.x - self.x), abs(obj.y - self.y)) <= obj.r + self.r


class Laser(Shot):
    def __init__(self, screen, gun):
        super(Laser, self).__init__()
        self.width = 5
        self.angle = 1
        self.live = 0

    def draw(self):
        pygame.draw.line(self.screen, RED, (self.x + 60 * math.cos(self.angle), self.y - 60 * math.sin(self.angle)),
                         (self.x + 1000 * math.cos(self.angle), self.y - math.sin(self.angle) * 1000), self.width)

    def move(self, event, gun):
        self.angle = -math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        self.x = gun.x
        self.y = gun.y

    def hit_test(self, obj):
        normal = [math.tan(self.angle), 1]
        return abs(((normal[0] * (obj.x - self.x) + normal[1] * (obj.y - self.y)) / (
                normal[0] ** 2 + normal[1] ** 2) ** 0.5)) <= obj.r


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450

    def move(self, key):
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
        new_ball = Ball(self.screen, Gun)
        new_ball.r += 5
        self.an = -math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = -math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        delta = (50 + self.f2_power)
        pygame.draw.polygon(self.screen, (2 * self.f2_power, 2 * self.f2_power, self.f2_power),
                            ((self.x, self.y), (self.x + delta * math.cos(self.an), self.y - delta * math.sin(self.an)),
                             (self.x + delta * math.cos(self.an) - 10 * math.sin(self.an),
                              self.y - delta * math.sin(self.an) - 10 * math.cos(self.an)),
                             (self.x - 10 * math.sin(self.an),
                              self.y - 10 * math.cos(self.an))))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Enemy:
    def __init__(self):
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        self.live = 1

    def move(self):
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
        """ Инициализация новой цели. """
        super(Target, self).__init__()
        self.r = rnd(10, 50)
        self.color = GAME_COLORS[rnd(0, 5)]

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Square(Enemy):
    def __init__(self):
        super(Square, self).__init__()
        self.color = BLACK
        self.live = 1
        self.r = rnd(5, 15)

    def jump(self):
        if 700 - self.r > self.x > 100 + self.r and 100 + self.r < self.y < 500 - self.r:
            if rnd(0, 100) < 25:
                rnd_x = rnd(-1, 1)
                rnd_y = rnd(-1, 1)
                self.x += rnd_x * 70
                self.y += rnd_y * 70

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_FONT = pygame.freetype.Font("arial.ttf", 40)
bullet = 0
score = 0
balls = []
squares = []

clock = pygame.time.Clock()
gun = Gun(screen)
laser = Laser(screen, gun)
targets = [Target() for _ in range(5)]
squares = [Square() for _ in range(2)]
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
            gun.targetting(event)
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
    gun.power_up()
pygame.quit()
