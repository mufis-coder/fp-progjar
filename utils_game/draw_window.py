import pygame
from utils_game.assets import STAT_FONT, BG_IMG, WIN_WIDTH, WIN_HEIGHT

# Function to create a button
def create_button(win, x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    # Mouse get pressed can run without an integer, but needs a 3 or 5 to indicate how many buttons
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(win, hovercolor, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(win, defaultcolor, (x, y, width, height))

def draw_window(win, birds, pipes, base, scores, player=-1, sinc_height=0, sinc_height_status=False):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score 1: " + str(scores[0]), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - 3*text.get_width(), 10))

    text = STAT_FONT.render("Score 2: " + str(scores[1]), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    if(sinc_height_status==False):
        for _, bird in birds.items():
            bird.draw(win)
    else:
        if(player!=-1):
            birds[player].draw_height_sinc(win, sinc_height)

    pygame.display.update()

def draw_wait_room(win, start_in):
    win.blit(BG_IMG, (0, 0))
    if(start_in == -2):
        text = STAT_FONT.render("Wait for Other Player", 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - text.get_width() - 70, int(WIN_HEIGHT/2)))
    else:
        text = STAT_FONT.render("Start in " + str(start_in), 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - text.get_width() - 178, int(WIN_HEIGHT/2)))

    pygame.display.update()