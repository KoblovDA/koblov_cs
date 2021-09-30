import math
import pygame
from pygame.draw import *

pygame.init()

orange = (200, 95, 45)
green = (14, 147, 37)
dark_green = (15, 83, 14)
blue = (161, 235, 245)
dark_blue = (14, 147, 145)
red = (235, 47, 68)
pink = (249, 194, 194)
brown = (147, 107, 14)
white = (255, 255, 255)
black = (0, 0, 0)

FPS = 30
screen = pygame.display.set_mode((455, 300))
rect(screen, blue, (0, 0, 455, 300))
rect(screen, green, (0, 150, 455, 150))

def home(size, x, y):
    rect (screen, brown, (x, y, size, 0.7 * size))
    rect (screen, black, (x, y, size, 0.7 * size), 1)
    rect (screen, dark_blue, (x + 0.35 * size, y + 0.22 * size, 0.3 * size, 0.26 * size))
    rect (screen, orange, (x + 0.35 * size, y + 0.22 * size, 0.3 * size, 0.26 * size), 1)
    polygon(screen, red, [(x, y), (x + size, y), (x + 0.48 * size,y - 0.48 * size)])
    polygon(screen, black, [(x, y), (x + size, y), (x + 0.48 * size,y - 0.48 * size)], 2)
def tree (size, x, y):
    rect (screen, black, (x, y, 0.2*size, size))
    circle (screen, dark_green, (x + 0.1*size, y - 0.8*size), 0.3*size)
    circle (screen, black, (x + 0.1*size, y - 0.8*size), 0.3*size, 1)
    circle (screen, dark_green, (x - 0.2*size, y - 0.5*size), 0.3*size)
    circle (screen, black, (x - 0.2*size, y - 0.5*size), 0.3*size, 1)
    circle (screen, dark_green, (x + 0.36*size, y - 0.5*size), 0.33*size)
    circle (screen, black, (x + 0.36*size, y - 0.5*size), 0.33*size, 1)
    circle (screen, dark_green, (x + 0.1*size, y - 0.3*size), 0.3*size)
    circle (screen, black, (x + 0.1*size, y - 0.3*size), 0.3*size, 1)
    circle (screen, dark_green, (x - 0.2*size, y - 0.1*size), 0.3*size)
    circle (screen, black, (x - 0.2*size, y - 0.1*size), 0.3*size, 1)
    circle (screen, dark_green, (x + 0.36*size, y - 0.1*size), 0.33*size)
    circle (screen, black, (x + 0.36*size, y - 0.1*size), 0.33*size, 1)
def clouds (size, x, y, color):
    for i in range (0, 4, 1):
        circle (screen, color, (x + i * size, y), size)
        circle (screen, black, (x + i * size, y), size, 1)
    for i in range (1, 3, 1):
        circle (screen, color, (x + i * size, y - size), size)
        circle (screen, black, (x + i * size, y - size), size, 1)
def sun (size, x, y, color):
    coordinates = []
    for i in range (0, 36, 1):
        coordinates.append((x + (size + (size/15)*(-1)**i)*math.cos(i*math.pi/18), y + (size+(size/15)*(-1)**i)*math.sin(i*math.pi/18)))
    polygon(screen, color, coordinates)
    polygon(screen, black, coordinates, 1)

home(110, 48, 160)
home(70, 260, 155)
tree (51, 197, 175)
tree (40, 360, 160)
clouds (16, 85, 45, white)
clouds (12, 227, 69, white)
clouds (16, 364, 60, white)
sun (22, 30, 27, pink)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()


