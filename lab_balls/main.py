import sys
import pygame
from pygame.locals import *
from random import randint, random
from colors import COLORS

# displaying the true size of the window, Windows only
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()
surface = pygame.display.set_mode((1700, 900)) #1700, 900
font = pygame.font.Font(None, 60)

FPS = 60
WIDTH = surface.get_width()
HEIGHT = surface.get_height()
SIZE = (WIDTH, HEIGHT)
MAX_RADIUS = 10
MIN_RADIUS = 4
MAX_SPEED = 10
NUM = [0, 50]

balls = [[pygame.Surface((2 * MAX_RADIUS, 2 * MAX_RADIUS), pygame.SRCALPHA, 32).convert_alpha()
        for i in range(NUM[j])] for j in range(2)]
clock = pygame.time.Clock()

def move(ball_type, cors, speeds, params):
    """shifts coordinates by speeds
    """
    for i in range(NUM[ball_type]):
        for j in range(2):
            if ball_type == 0:
                if cors[0][i][j] + speeds[0][i][j] > SIZE[j] - params[0][i][0]:
                    speeds[0][i][j] = -speeds[0][i][j]
                    speeds[0][i][not j] += randint(-MAX_SPEED // 10, MAX_SPEED // 10)
                    cors[0][i][j] += speeds[0][i][j] + 2*(SIZE[j] - params[0][i][0] - cors[0][i][j])
                elif cors[0][i][j] + speeds[0][i][j] < params[0][i][0]:
                    speeds[0][i][j] = -speeds[0][i][j]
                    speeds[0][i][not j] += randint(-MAX_SPEED // 10, MAX_SPEED // 10)
                    cors[0][i][j] += speeds[0][i][j] + 2*(params[0][i][0] - cors[0][i][j])
                else:
                    cors[0][i][j] += speeds[0][i][j]
            else:
                if cors[1][i][j] + speeds[1][i] * (1 - j *2) * (cors[1][i][not j] - params[1][i][1][not j]) / (
                                   (cors[1][i][0] - params[1][i][1][0]) ** 2
                                   + (cors[1][i][1] - params[1][i][1][1]) ** 2) ** 0.5 > SIZE[j] - params[1][i][0] or \
                   cors[1][i][j] + speeds[1][i] * (1 - j *2) * (cors[1][i][not j] - params[1][i][1][not j]) / (
                                   (cors[1][i][0] - params[1][i][1][0]) ** 2
                                   + (cors[1][i][1] - params[1][i][1][1]) ** 2) ** 0.5 < params[1][i][0]:
                    params[1][i][1][not j] = 2 * cors[1][i][not j] - params[1][i][1][not j]
                else:
                    cors[1][i][j] += speeds[1][i] * (1 - j *2) * (cors[1][i][not j] - params[1][i][1][not j]) / (
                                     (cors[1][i][0] - params[1][i][1][0]) ** 2
                                     + (cors[1][i][1] - params[1][i][1][1]) ** 2) ** 0.5
    return cors

def click(score, pos, cors, speeds, params):
    """changing the score
    """
    for j in range(2):
        for i in range(NUM[j]):
            if (pos[0] - cors[j][i][0]) ** 2 + (pos[1] - cors[j][i][1]) ** 2 <= params[j][i][0] ** 2:
                if j == 0:
                    score += MAX_RADIUS // params[j][i][0]
                else:
                    score += 2 * MAX_RADIUS // params[j][i][0]
    return score

cors = [[], []]       # coordinates of balls
speeds = [[], []]     # speeds of balls
params = [[], []]     # list of radii, the name "params" - a reserve for the future

score = 0
missed = 0
end = False

# Initializing balls
for i in range(NUM[0]):
    params[0].append([randint(MIN_RADIUS, MAX_RADIUS)])
    cors[0].append([randint(params[0][i][0], WIDTH - params[0][i][0]), randint(params[0][i][0], HEIGHT - params[0][i][0])])
    speeds[0].append([(random() - 0.5) * 2 * MAX_SPEED, (random() - 0.5) * 2 * MAX_SPEED])
    pygame.draw.circle(balls[0][i], COLORS[randint(0, len(COLORS) - 1)], (params[0][i][0], params[0][i][0]), params[0][i][0]) 

for i in range(NUM[1]):
    params[1].append([randint(MIN_RADIUS, MAX_RADIUS), [randint(-WIDTH // 2, WIDTH // 2 * 3), randint(-HEIGHT // 2, HEIGHT // 2 * 3)]])
    cors[1].append([randint(params[1][i][0], WIDTH - params[1][i][0]), randint(params[1][i][0], HEIGHT - params[1][i][0])])
    speeds[1].append((random() - 0.5) * 2 * MAX_SPEED)
    pygame.draw.circle(balls[1][i], COLORS[randint(0, len(COLORS) - 1)], (params[1][i][0], params[1][i][0]), params[1][i][0])

while not end:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if score < click(score, ev.pos, cors, speeds, params):
                score = click(score, ev.pos, cors, speeds, params)
            else:
                missed += 1
                if missed > 2:
                    end = True
    surface.fill((0, 0, 0))
    clock.tick(FPS)
    
    text_score = font.render('Score: ' + str(score), True, [255, 255, 255])
    text_missed = font.render('Missed: ' + str(missed), True, [255, 255, 255])
    surface.blit(text_score, (10, 10))
    surface.blit(text_missed, (10, 60))
    for j in range(2):
        cors = move(j, cors, speeds, params)
        for i in range(NUM[j]):
            surface.blit(balls[j][i], [cors[j][i][0] - params[j][i][0], cors[j][i][1] - params[j][i][0]])
    pygame.display.flip()

text_game_over = font.render('Game over!', True, [255, 255, 255])
surface.blit(text_game_over, (WIDTH // 2 - 120, HEIGHT // 2 - 20))

f = open('ratings.txt', 'a+')
print('Enter Your Name: ')
name = input()
f.write( 'Name: ' + str(name))
f.write(', Score: ' + str(score))
f.write('\n')
f.close()

"""
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
        elif ev.type == pygame.KEYDOWN:
            
    clock.tick(FPS)
    pygame.display.flip()
"""





