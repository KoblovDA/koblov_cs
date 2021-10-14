from pygame.draw import *
from random import randint
import pygame.freetype

pygame.init()
GAME_FONT = pygame.freetype.Font("arial.ttf", 40)
screen = pygame.display.set_mode((800, 600))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (160, 70, 70)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]  # цвета шариков
MAX, MIN, FINE = 20, 10, -2  # количество очков за попадание в маленький, большой шарик, штраф за промах


def new_ball():
    x_0 = randint(200, 700)
    y_0 = randint(200, 500)
    r_0 = randint(30, 60)
    u_x = randint(-20, 20)
    u_y = randint(-20, 20)
    color = COLORS[randint(0, 5)]
    return [x_0, y_0, r_0, u_x, u_y, 0, color]


def draw_ball(scr, parameters):
    circle(scr, parameters[6], (parameters[0], parameters[1]), parameters[2])


def change_of_color(clr, rand):
    new_color = [clr[0], clr[1], clr[2]]
    for i in range(0, 3):
        colour = new_color[i]
        colour += randint(-rand, rand)
        if colour < rand + 1:
            colour += rand
        elif colour > 254 - rand:
            colour -= rand
        new_color[i] = colour
    return new_color[0], new_color[1], new_color[2]


balls = []
for i in range(0, 10):
    balls.append([0, 0, 0, 0, 0, 0, 0])
pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = 0
success = -1
global_success = -1
time_of_game = 0
num_of_success = -1
while not finished:
    FPS = 30
    clock.tick(FPS)
    time_of_game += FPS
    screen.fill(WHITE)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (time_of_game >= 10000):
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x = event.pos[0]
            event.y = event.pos[1]
            for i in range(0, 10):
                x_ball, y_ball, r_ball = balls[i][0], balls[i][1], balls[i][2]
                if (event.x - x_ball) ** 2 + (event.y - y_ball) ** 2 < r_ball ** 2:
                    num_of_success = i
                    if r_ball < 45:
                        score += MAX
                    else:
                        score += MIN
                    success = 1
                    global_success = 1
            if success != 1:
                success = 0
                global_success = 0
                score += FINE
    if global_success == 1:
        text_surface, rect = GAME_FONT.render("Good hit) Score: " + str(score), FONT_COLOR)
        screen.blit(text_surface, (50, 50))
    else:
        if global_success == 0:
            text_surface, rect = GAME_FONT.render("Bad hit... Score: " + str(score), FONT_COLOR)
            screen.blit(text_surface, (50, 50))
        else:
            text_surface, rect = GAME_FONT.render("Click on the ball! Score: 0", FONT_COLOR)
            screen.blit(text_surface, (50, 50))
    for i in range(0, 10):
        balls[i][5] += 1
        if (balls[i][5] >= 200) or (balls[i][3] == 0) or (num_of_success == i):
            balls[i] = new_ball()
        else:
            balls[i][0] += balls[i][3]
            balls[i][1] += balls[i][4]
            balls[i][6] = change_of_color(balls[i][6], 10)
        if balls[i][0] + balls[i][2] > 799:
            balls[i][3] = -balls[i][3]
            balls[i][0] -= 10
        elif balls[i][0] - balls[i][2] < 1:
            balls[i][3] = -balls[i][3]
            balls[i][0] += 10
        if balls[i][1] + balls[i][2] > 599:
            balls[i][4] = -balls[i][4]
            balls[i][0] -= 10
        elif balls[i][1] - balls[i][2] < 1:
            balls[i][4] = -balls[i][4]
            balls[i][0] += 10
        draw_ball(screen, balls[i])
    num_of_success = -1
    success = 0
    pygame.display.update()
pygame.quit()
