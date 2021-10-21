from random import randint
RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN = (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255), (
    0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (200, 70, 130)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]  # цвета шариков
MAX, MIN, FINE = 20, 10, -5  # количество очков за попадание в маленький, большой шарик, штраф за промах
NUMBER_OF_BALLS = 4
space = (800, 600)
score = 0
success = -1  # Если клик успешен, то 1, иначе 0. До клика равна -1. Далее 1 или 0.
global_success = -1  # Запоминает последний клик. Аналогична success, но не зануляется после обработки события
time_of_game = 0
num_of_success = -1

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


def new_square():
    """
    Аналогично с шариком, только создаёт переменные для квадратиков, которые меньше и быстрее. x0, y0 задают
    центр квадратика
    """
    x_0 = randint(200, 700)
    y_0 = randint(200, 500)
    r_0 = randint(10, 20)
    u_x = randint(-40, 40)
    u_y = randint(-40, 40)
    color = COLORS[randint(0, 5)]
    return [x_0, y_0, r_0, u_x, u_y, 0, color]


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


def init():
    global balls, squares
    balls = [new_ball() for _ in range(NUMBER_OF_BALLS)]
    squares = [new_square() for _ in range(NUMBER_OF_BALLS)]


def tick():
    for i in range(0, NUMBER_OF_BALLS):
        if balls[i][5] >= 200 or num_of_success == i:
            balls[i] = new_ball()
        else:
            balls[i][0] += balls[i][3]
            balls[i][1] += balls[i][4]
            balls[i][6] = change_of_color(balls[i][6], 8)
        if squares[i][5] >= 200 or num_of_success == NUMBER_OF_BALLS + i:
            squares[i] = new_square()
        else:
            squares[i][0] += squares[i][3] + randint(-15, 15)
            squares[i][1] += squares[i][4] + randint(-15, 15)
            squares[i][6] = change_of_color(squares[i][6], 12)
        x, y, r = balls[i][0], balls[i][1], balls[i][2]
        if x + r > space[0] or x - r < 0:
            balls[i][3] = -balls[i][3]
        if y + r > space[1] or y - r < 0:
            balls[i][4] = -balls[i][4]
        x, y, r = squares[i][0], squares[i][1], squares[i][2]
        if x + r > space[0] or x - r < 0:
            squares[i][3] = -squares[i][3]
        if y + r > space[1] or y - r < 0:
            squares[i][4] = -squares[i][4]


def handler(position):
    global success, global_success, num_of_success, score
    x_pos = position[0]
    y_pos = position[1]
    for i in range(0, NUMBER_OF_BALLS):
        x_ball, y_ball, r_ball = balls[i][0], balls[i][1], balls[i][2]
        # Попадание клика в область шарика. Если попал - num_of_success присваивается номер этого шарика.
        if (x_pos - x_ball) ** 2 + (y_pos - y_ball) ** 2 <= r_ball ** 2:
            num_of_success = i
            # Разветвление в зависимости от размера шарика
            if r_ball < 45:
                score += MAX
            else:
                score += MIN
            success = 1
            global_success = 1
    for i in range(0, NUMBER_OF_BALLS):
        x_square, y_square, r_square = squares[i][0], squares[i][1], squares[i][2]
        # Попадание клика в область шарика. Если попал - num_of_success присваивается номер этого шарика.
        if abs(x_pos - x_square) <= r_square and abs(y_pos - y_square) <= r_square:
            num_of_success = i + NUMBER_OF_BALLS
            # Разветвление в зависимости от размера шарика
            score += 2 * MAX
            success = 1
            global_success = 1
    if success != 1:
        success = 0
        global_success = 0
        score += FINE  # Штраф за непопадание
