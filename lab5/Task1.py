from pygame.draw import *
from random import randint
import pygame.freetype

pygame.init()
GAME_FONT = pygame.freetype.Font("arial.ttf", 60)
screen = pygame.display.set_mode((900, 900))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (160, 70, 70)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]  # цвета шариков
font = pygame.font.SysFont('Arial', 10, False, False)
x_0, y_0, r_0 = 0, 0, 0
MAX, MIN, FINE = 20, 10, -2  # количество очков за попадание в маленький, большой шарик, штраф за промах


def new_ball():
    global x_0, y_0, r_0
    x_0 = randint(200, 700)
    y_0 = randint(200, 500)
    r_0 = randint(30, 60)


def draw_ball(scr):
    color = COLORS[randint(0, 5)]
    circle(scr, color, (x_0, y_0), r_0)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
points = 0
success = -1
success_in_time = -1
time_of_game = 0
time_of_ball = 0
u_x = 0
u_y = 0
while not finished:
    FPS = randint(1, 2)
    clock.tick(FPS)
    time_of_game += FPS
    screen.fill(BLACK)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (time_of_game >= 100):
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x = event.pos[0]
            event.y = event.pos[1]
            if (event.x - x_0) ** 2 + (event.y - y_0) ** 2 < r_0 ** 2:
                if r_0 < 45:
                    points += MAX
                else:
                    points += MIN
                success = 1
                success_in_time == 1
            else:
                success = 0
                points += -FINE
    if success == 1:
        text_surface, rect = GAME_FONT.render("Good hit) Points: " + str(points), FONT_COLOR)
        screen.blit(text_surface, (70, 120))
    elif success == -0:
        text_surface, rect = GAME_FONT.render("Bad hit... Points: " + str(points), FONT_COLOR)
        screen.blit(text_surface, (70, 120))
    time_of_ball += 1
    if (time_of_ball >= 10) or (u_x == 0) or (success_in_time == 1):
        new_ball()
        time_of_ball = 0
        u_x = randint(50, 120)
        u_y = randint(50, 120)
    else:
        x_0 += u_x
        y_0 += u_y
    draw_ball(screen)
    success_in_time = -1
    pygame.display.update()
pygame.quit()
