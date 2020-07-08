import pygame
from pygame.locals import *
import random
import time,sys


class SnakeNibble:
    """Move snake. When the snake eats fruit, the body will become longer, and the game will end when it hits the wall or hits itself"""
    def __init__(self,width=400,edge=20):
        self.width = self.height = 400 # screen size
        self.edge = edge # snake size
        self.ball = pygame.Surface((edge, edge)) # Surface
    
    def makeSnake(self):
        '''Create snake initial direction right'''
        self.ball.fill((0,0,255)) # blue
        ballrect = self.ball.get_rect() 
        a = self.edge * 5
        snake = []
        for i in range(3):
            ballrect2 = ballrect.copy() 
            ballrect2.left += a
            ballrect2.top = 100
            a -= self.edge
            snake.append(ballrect2)
        return snake

    def move(self,snake,direct):
        """Move in the direction and return to the tail of the snake before updating"""
        for i in range(len(snake)):
            if i==0: 
                rect = snake[0].copy()
                temp = self._get_nextRect(rect,direct)
        snake.insert(0,temp) 
        endPop = snake.pop() 
        return endPop

    def strike(self,snake,food):
        '''Snake impact detection'''
        # Hit the wall
        if snake[0].left < 0 or snake[0].right > self.width: return 0
        if snake[0].top < 0 or snake[0].bottom > self.height: return 0
        # Bump into myself
        for sr in snake[1:]:
            if sr.colliderect(snake[0]):
                return 0
        # eat
        if food.colliderect(snake[0]):
            return 1
        return 2 

    def _get_nextRect(self,rect,direct):
        """Snake gets the new position of the head"""
        if direct == 0: rect.top += self.edge # under
        elif direct == 1: rect.top -= self.edge # up
        elif direct == 2: rect.left += self.edge # right
        elif direct == 3: rect.left -= self.edge # left
        return rect
        
 
class Food:
    """Randomly generated food"""
    def __init__(self,width=400,edge=20):
        self.width = self.height = 400
        self.edge = edge
        self.food = pygame.Surface((self.edge, self.edge)) # surface 

    def get_food(self):
        """Generate food rect object"""
        self.food.fill((220,20,60)) # red
        fr = self.food.get_rect() 
        return fr
    
    def get_foodpos(self,food,snake):
        '''food new position'''
        while True:
            food.left, food.top = random.randrange(self.edge,self.height,self.edge),random.randrange(self.edge,self.height,self.edge) 
            foodpos = True
            for sn in snake: 
                if food.colliderect(sn):
                    foodpos = False
                    break
            if foodpos == True:
                break
        if foodpos == True: 
            return True

class Background:
    def __init__(self,width=400,edge=20):
        self.width = self.height = 400
        self.edge = edge
        self.scoref = pygame.font.SysFont('Arial', 30) # typeface

    def drawGrid(self,surface):
        
        rows = self.width // self.edge
        sizeBtwn = self.edge
        x,y = 0,0
        for _ in range(rows):
            x += sizeBtwn
            y += sizeBtwn
            pygame.draw.line(surface,(219,112,147),(x,0),(x,self.width))
            pygame.draw.line(surface, (219,112,147),(0,y),(self.width,y))

def main(best):
    """Initialize and run in a loop until there is a return"""
    # initialization
    pygame.init()
    direct = 2 
    validDirect = direct 
    edge = 20 # lattice size
    black = 0,0,0 # background color
    width,height = 400,400 
    screen = pygame.display.set_mode((width,height)) 
    pygame.display.set_caption('Snake')
    
    
    # snake
    s = SnakeNibble(width,edge) # snake size = lattice size
    snake = s.makeSnake() 
    # food
    f = Food(width,edge) # food size = lattice size
    foodr = f.get_food() 
    f.get_foodpos(foodr,snake) 
    # lattice
    b = Background(width,edge)

    c = 0 # count
    dt = 0 # Timing
    score = 0 # Score
    going = True 
    endPop = None # snake tail
    interval = 300 
    clock = pygame.time.Clock() 
    while going:
        lastt = clock.tick(60) 
        dt += lastt 
        c += 1
        print('Cycles %d, last time %d，now time %d millisecond'%(c,lastt,dt)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP and validDirect != 0: direct = 1 
                elif event.key == K_DOWN and validDirect != 1: direct = 0 
                elif event.key == K_LEFT and validDirect != 2: direct = 3 
                elif event.key == K_RIGHT and validDirect != 3: direct = 2 

        
        screen.fill(black)
        
        if dt > interval: 
            validDirect = direct
            dt = 0 
            endPop = s.move(snake,direct)
       
        for i in snake:
            screen.blit(s.ball, i)
        
        
        b.drawGrid(screen) 
        
        scoret=b.scoref.render(str(score), True, (255, 255, 255)) 
        screen.blit(scoret, (0, 0)) 
        scoret2=b.scoref.render('best:'+str(best), True, (255, 255, 255)) 
        screen.blit(scoret2, (width-6*edge, 0)) 
        #food
        screen.blit(f.food, foodr) 
        
        clli = s.strike(snake,foodr)
        if clli == 0: 
            going = False
        elif clli == 1: 
            snake.append(endPop) 
            score += 1
            if not f.get_foodpos(foodr,snake): going = False 
        
        pygame.display.flip() 
    
    
    if score > best:
        return score
    else:
        return best
                
if __name__ == '__main__':
    best = 0 
    while True:
        best = main(best) 
        time.sleep(1)
