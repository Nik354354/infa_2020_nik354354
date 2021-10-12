import pygame, sys
from pygame.draw import *

def draw_ellipse(surface, x, y, width, height, angle, color):
    """draw an ellipse
    
    """
    ellipse_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
    pygame.draw.ellipse(ellipse_surface, color, (0, 0, width, height))  
    rot_surface = pygame.transform.rotate(ellipse_surface, angle)
    rcx, rcy = rot_surface.get_rect().center
    surface.blit(rot_surface, (x - rcx, y - rcy))

def bird(surface, x, y, size, color):
    """draw a bird
    
    """
    draw_ellipse(surface, x, y, 40*size, 10*size, 45, color)
    draw_ellipse(surface, x - 25*size, y, 40*size, 15*size, -45, color)
    
