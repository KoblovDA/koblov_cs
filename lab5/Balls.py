from pygame.draw import *
import pygame.freetype
import lab5.model as model

pygame.init()
model.init()
GAME_FONT = pygame.freetype.Font("arial.ttf", 40)
screen = pygame.display.set_mode(model.space)
global time_of_game, success, global_success, score, num_of_success


def draw_ball(scr, parameters):
    """
    Принимает экран и параметры шарика (записанные в форме, как в прошлой функции), то есть использует
    координаты, цвет и радиус шарика
    """
    circle(scr, parameters[6], (parameters[0], parameters[1]), parameters[2])


def draw_square(scr, parameters):
    x_0 = parameters[0]
    y_0 = parameters[1]
    r_0 = parameters[2]
    pygame.draw.rect(scr, parameters[6], (x_0 - r_0, y_0 - r_0, 2 * r_0, 2 * r_0))


def print_score(scr):
    """
    Вывод надписи об успешности попадания. Использует переменную global_success (данные о последнем попадании)
    и число очков score
    """
    global global_success, score
    if model.global_success == 1:
        text_surface, rect = GAME_FONT.render("Good hit) Score: " + str(model.score), model.FONT_COLOR)
        scr.blit(text_surface, (50, 50))
    else:
        if model.global_success == 0:
            text_surface, rect = GAME_FONT.render("Bad hit... Score: " + str(model.score), model.FONT_COLOR)
            scr.blit(text_surface, (50, 50))
        else:
            text_surface, rect = GAME_FONT.render("Click on the ball! Score: 0", model.FONT_COLOR)
            scr.blit(text_surface, (50, 50))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    FPS = 30
    clock.tick(FPS)
    model.time_of_game += FPS
    screen.fill(model.WHITE)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (
                model.time_of_game >= 100000):  # Прерывание игры через некоторое время или при выходе
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x = event.pos[0]
            event.y = event.pos[1]
            model.handler((event.x, event.y))
    print_score(screen)
    model.tick()
    for i in range(model.NUMBER_OF_BALLS):
        draw_ball(screen, model.balls[i])
        draw_square(screen, model.squares[i])
    model.num_of_success = -1  # Сброс номера шарика, по которому мы попали
    model.success = 0
    pygame.display.update()
pygame.quit()
