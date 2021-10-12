import pygame, sys
from pygame.draw import *
import math as m

def hill_1(surface, color):
    """draws a hill of the first type
    
    """
    u_hill_x = 0
    u_hill_xy = [0]*801
    while u_hill_x < 10:
        y = -u_hill_x*3 + 250
        u_hill_xy[u_hill_x] = (u_hill_x,y)
        u_hill_x += 1
    while u_hill_x < 165:
        y = -((u_hill_x-10)**2)/200 + 220
        u_hill_xy[u_hill_x] = (u_hill_x,y)
        u_hill_x += 1
    while u_hill_x < 195:
        y = (u_hill_x-165)*0.4 + 101
        u_hill_xy[u_hill_x] = (u_hill_x,y)
        u_hill_x += 1
    while u_hill_x < 215:
        y = (u_hill_x-195)*1.2 + 113
        u_hill_xy[u_hill_x] = (u_hill_x,y)
        u_hill_x += 1
    while u_hill_x < 501:
       y = -((u_hill_x-350)**2/200 - 228)
       u_hill_xy[u_hill_x] = (u_hill_x,y)
       u_hill_x += 1
    while u_hill_x < 521:
        y = (u_hill_x-165)*0.1 + 81
        u_hill_xy[u_hill_x] = (u_hill_x,y)
        u_hill_x += 1
    while u_hill_x < 800:
       y = -((u_hill_x-700)**2/200 - 280)
       u_hill_xy[u_hill_x] = (u_hill_x,y)
       u_hill_x += 1
    u_hill_xy[800] = (800,300)
    polygon(surface, color, (u_hill_xy), 0)

def hill_2(surface, color):
    """draws a hill of the second type
    
    """
    sin_x = 1
    sin_xy = [0]*801
    sin_xy[0] = (0,360)
    while sin_x < 800:
        y = 20*m.sin(0.1*sin_x) - 0.05*sin_x + 300
        sin_xy[sin_x] = (sin_x,y)
        sin_x += 1
    sin_xy[800] = (801,330)
    polygon(surface, color, (sin_xy), 0)








