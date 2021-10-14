from pygame.draw import *
from random import randint
import pygame.freetype
pygame.init()
GAME_FONT = pygame.freetype.Font("arial.ttf", 60)
FPS = 2
screen = pygame.display.set_mode((900, 900))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (160, 70, 70)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
font = pygame.font.SysFont('Arial', 10, False, False)
x_0, y_0, r_0 = 0, 0, 0


def new_ball():
    global x_0, y_0, r_0
    x_0 = randint(200, 700)
    y_0 = randint(200, 500)
    r_0 = randint(30, 50)


def draw_ball(scr):
    color = COLORS[randint(0, 5)]
    circle(scr, color, (x_0, y_0), r_0)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
points = 0
success = -1
time = 0
while not finished:
    clock.tick(FPS)
    time += FPS
    screen.fill(BLACK)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (time >= 100):
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x = event.pos[0]
            event.y = event.pos[1]
            if (event.x - x_0) ** 2 + (event.y - y_0) ** 2 < r_0 ** 2:
                print('Good hit)')
                points += 1
                success = 1
            else:
                print('Bad hit(')
                success = 0
    if success == 1:
        text_surface, rect = GAME_FONT.render("Good hit) Points: " + str(points), FONT_COLOR)
        screen.blit(text_surface, (70, 120))
    elif success == -0:
        text_surface, rect = GAME_FONT.render("Bad hit... Points: " + str(points), FONT_COLOR)
        screen.blit(text_surface, (70, 120))
    new_ball()
    draw_ball(screen)
    pygame.display.update()
pygame.quit()
