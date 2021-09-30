import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 600))
rect(screen, (220, 220, 220), (0, 0, 600, 600))

yellow = (254, 252, 0)
black = (0, 0, 0)
red = (254, 0, 0)
blue = (0, 0, 255)


circle(screen, yellow, (300, 300), 150)
circle(screen, black, (300, 300), 150, 2)

circle(screen, red, (250, 250), 30)
circle(screen, black, (250, 250), 30, 1)
circle(screen, black, (250, 250), 15)

circle(screen, red, (350, 250), 25)
circle(screen, black, (350, 250), 25, 1)
circle(screen, black, (350, 250), 15)
polygon(screen, black, [(260, 370), (350, 370), (370, 400), (240, 400)])

polygon(screen, black, [(210, 150), (280, 220), (280, 240), (210, 170)])
polygon(screen, black, [(370, 145), (322, 224), (322, 244), (382, 160)])
polygon(screen, blue, [(270, 330), (302, 300), (342, 330)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
