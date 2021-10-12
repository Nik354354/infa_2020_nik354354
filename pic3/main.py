import pygame, sys
from pygame.draw import *
from colors import *
from birds import bird
from hills import *

# displaying the true size of the window, Windows only
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 532))

# background
screen.fill(PEACH)
polygon(screen, PURPLE, [(0,362), (800,346),(800,532), (0,532)], 0)
polygon(screen, DESERT_SAND, [(0,115), (800,115),(800,230), (0,230)], 0)
circle(screen, YELLOW, (540, 120), 50) # the sun

# draw hills
hill_1(screen, CARROT)
hill_2(screen, CARMINE)

# draw birds
bird(screen, 400, 90, 1, DARK_BROWN)
bird(screen, 300, 180, 1.5, DARK_BROWN)
bird(screen, 100, 400, 2, DARK_BROWN)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
