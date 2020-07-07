import pygame
from pygame.locals import *
import random
pygame.init()

edge = 20 
screenColor = 0, 0, 0
width,height = 400,400 
screen = pygame.display.set_mode((width,height)) 
pygame.display.set_caption('Snake') 


grid = pygame.Surface((edge, edge)) 
gridColor = (0,0,255) 
grid.fill(gridColor) 
gr = grid.get_rect() 
gr.left, gr.top = random.randrange(10,width,10),random.randrange(10,height,10) 

def get_nextRect(rect,direct,sWidth):
    if direct == 0:
        rect.top += sWidth
    elif direct == 1: 
        rect.top -= sWidth
    elif direct == 2: 
        rect.left += sWidth
    elif direct == 3: 
        rect.left -= sWidth
    return rect

direct  = 2 
going = True 
clock = pygame.time.Clock()
while going:
    clock.tick(10) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
        elif event.type == KEYDOWN:
            if event.key == K_UP and direct != 0:direct = 1 
            elif event.key == K_DOWN and direct != 1:direct = 0 
            elif event.key == K_LEFT and direct != 2:direct = 3 
            elif event.key == K_RIGHT and direct != 3:direct = 2 
            elif event.key == K_0:
                    going = False 
    
    if gr.left < 0: direct = 2
    if gr.right > width: direct = 3
    if gr.top < 0: direct = 0
    if gr.bottom > height: direct = 1 
    screen.fill(screenColor) 
    gr = get_nextRect(gr,direct,edge) 
    screen.blit(grid, gr) 
    pygame.display.flip() 
pygame.quit() 








