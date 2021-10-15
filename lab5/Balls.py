from pygame.draw import *
from random import randint
import pygame.freetype

pygame.init()
GAME_FONT = pygame.freetype.Font("arial.ttf", 40)
screen = pygame.display.set_mode((800, 600))
RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN = (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255), (
    0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (200, 70, 130)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]  # цвета шариков
MAX, MIN, FINE = 20, 10, -5  # количество очков за попадание в маленький, большой шарик, штраф за промах
NUMBER_OF_BALLS = 10


def new_ball():
    """
    Функция создаёт новый шарик с рандомными параметрами в указанных диапазонах -
    x_0, y_0 - координаты, r_0 - радиус шарика, u_x и u_y - скорости шарика по указанным осям.
    color - цвет шарика из листа цветов, указанных ранее.
    Выдаёт лист данных, который характеризует его, который далее в программе используется в листе со всеми шариками
    """
    x_0 = randint(200, 700)
    y_0 = randint(200, 500)
    r_0 = randint(30, 60)
    u_x = randint(-20, 20)
    u_y = randint(-20, 20)
    color = COLORS[randint(0, 5)]
    return [x_0, y_0, r_0, u_x, u_y, 0, color]


def draw_ball(scr, parameters):
    """
    Принимает экран и параметры шарика (записанные в форме, как в прошлой функции), то есть использует
    координаты, цвет и радиус шарика
    """
    circle(scr, parameters[6], (parameters[0], parameters[1]), parameters[2])


def change_of_color(clr, rand):
    """
    Функция, добавляющая отличительную черту геймплея - малые колебания цвета шариков со временем.
    Принимает исходный цвет и число, которое характеризует размах колебаний
    """
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


balls = []  # Массив, хранящий данные о шарике. Порядок такой же, как в new_ball.
for i in range(0, NUMBER_OF_BALLS):
    balls.append([0, 0, 0, 0, 0, 0, 0])
pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = 0
success = -1  # Если клик успешен, то 1, иначе 0. До клика равна -1. Далее 1 или 0.
global_success = -1  # Запоминает последний клик. Аналогична success, но не зануляется после обработки события
time_of_game = 0
num_of_success = -1
while not finished:
    FPS = 30
    clock.tick(FPS)
    time_of_game += FPS
    screen.fill(WHITE)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (
                time_of_game >= 100000):  # Прерывание игры через некоторое время или при выходе
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x = event.pos[0]
            event.y = event.pos[1]
            for i in range(0, NUMBER_OF_BALLS):
                x_ball, y_ball, r_ball = balls[i][0], balls[i][1], balls[i][2]
                # Попадание клика в область шарика. Если попал - num_of_success присваивается номер этого шарика.
                if (event.x - x_ball) ** 2 + (event.y - y_ball) ** 2 < r_ball ** 2:
                    num_of_success = i
                    # Разветвление в зависимости от размера шарика
                    if r_ball < 45:
                        score += MAX
                    else:
                        score += MIN
                    success = 1
                    global_success = 1
            if success != 1:
                success = 0
                global_success = 0
                score += FINE  # Штраф за непопадание
    # Вывод надписи об успешности попадания. Использует перемену global_success (данные о последнем попадании)
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
    for i in range(0, NUMBER_OF_BALLS):
        balls[i][5] += 1
        if (balls[i][5] >= 200) or (balls[i][3] == 0) or (num_of_success == i):
            # Замена шарика на новый, если существовал слишком долго, имел нулевую скорость или по нему попали
            balls[i] = new_ball()
        else:
            balls[i][0] += balls[i][3]
            balls[i][1] += balls[i][4]
            balls[i][6] = change_of_color(balls[i][6], NUMBER_OF_BALLS)
        # Далее идут четыре условия, при которых шарик должен оттолкнуться от стенки - если его край к ней прижался
        if balls[i][0] + balls[i][2] > 799:
            balls[i][3] = -balls[i][3]
        elif balls[i][0] - balls[i][2] < 1:
            balls[i][3] = -balls[i][3]
        if balls[i][1] + balls[i][2] > 599:
            balls[i][4] = -balls[i][4]
        elif balls[i][1] - balls[i][2] < 1:
            balls[i][4] = -balls[i][4]
        draw_ball(screen, balls[i])
    num_of_success = -1  # Сброс номера шарика, по которому мы попали
    success = 0
    pygame.display.update()
pygame.quit()
