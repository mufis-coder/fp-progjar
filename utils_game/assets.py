import pygame
import os

POSX1 = 235
POSY1 = 200
POSX2 = 245
POSY2 = 300
WIN_WIDTH = 500
WIN_HEIGHT = 700

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

BIRD_IMGS = [[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/birds/red", "bird1.png"))), 
			pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/birds/red", "bird2.png"))), 
			pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/birds/red", "bird3.png")))], 
            [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/birds/black", "bird1.png"))), 
			pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/birds/black", "bird2.png"))), 
			pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/birds/black", "bird3.png")))]]

font = pygame.font.SysFont("comicsans", 40)
smallfont = pygame.font.SysFont("comicsans", 14)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
red = (255, 21, 0)
lightred= (255, 140, 0)
green = (0, 255, 64)
lightgreen= (0, 255, 191)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)