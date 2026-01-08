import pygame
import math
pygame.init()

screen = pygame.display.set_mode((640, 640))

mario_img = pygame.image.load('mario.png').convert()

x = 0
y = 0
running = True
while running:
    screen.blit(mario_img, (x, 30))
    screen.blit(mario_img, (y, 30))
    y+=0.025
    x+=0.025
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
