import sys
import pygame
import os
import random

sys.path.append('/object_game/')

from object_game.pipe import Pipe
from object_game.bird import Bird
from object_game.base import Base

WIN_WIDTH = 500
WIN_HEIGHT = 700
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)

    pygame.display.update()

def main():
    posX = random.randint(230, 250)
    posY = random.randint(100, 500)

    bird = Bird(posX, posY)
    base = Base(630)
    pipes = [Pipe(600)]
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    score = 0
    
    run = True
    while(run):
        clock.tick(30)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
                pygame.quit()
                quit()
        
        pipe_ind = 0
        if(len(pipes)>1 and bird.x>pipes[0].x+pipes[0].PIPE_TOP.get_width()):
            pipe_ind = 1
        else:
            run = False
            break

        #move bird
        bird.move()
        bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
                break
            if (not pipe.passed and pipe.x<bird.x):
                pipe.passed = True
                add_pipe = True
            if (pipe.x+pipe.PIPE_TOP.get_width() < 0):
                rem.append(pipe)
            
            pipe.move()
        
        if (add_pipe):
            score += 1
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        if (bird.y + bird.img.get_height() >= 630 or bird.y < 0):
            run = False
        
        base.move()
        draw_window(win, bird, pipes, base, score)
