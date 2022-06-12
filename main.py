import sys
import pygame
from datetime import date
import socket
import select
import sys
from threading import Thread

PLAYER = 0
KEYJUMP = pygame.K_SPACE

sys.path.append('/object_game/')
sys.path.append('/utils_game/')
pygame.init()

from object_game.pipe import Pipe
from object_game.bird import Bird
from object_game.base import Base
from utils_game.sent_data import data_send
from utils_game.sent_data import send_msg
from utils_game.sent_data import recv_msg
from utils_game.draw_window import draw_window, draw_wait_room, create_button
from utils_game.assets import smallfont, slategrey, lightgrey, font, blackish
from utils_game.assets import POSX1, POSY1, POSX2, POSY2, WIN_WIDTH, WIN_HEIGHT
from utils_game.assets import BIRD_IMGS, STAT_FONT, BG_IMG

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
# ip_address = '13.229.230.226'
# port = 5555
server.connect((ip_address, port))

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

# Start menu returns true until we click the Start button
def start_menu(win, clock):
    startText = STAT_FONT.render("FLAPPY BIRD", True, slategrey)
    today = date.today()
    todayText = "Today is " + today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%d") + \
                ", " + today.strftime("%Y")
    todayText = smallfont.render(todayText, True, slategrey)

    while True:
        win.blit(BG_IMG, (0, 0))
        # (image variable, (left, top))
        win.blit(todayText, (5, 10))
        # The centered Text
        win.blit(startText, ((WIN_WIDTH - startText.get_width()) / 2, 100))

        # start button (left, top, width, height)
        start_button = create_button(win, 200, WIN_HEIGHT/2 - 8 , 120, 40, lightgrey, slategrey)

        if start_button:
            main(win, clock)

        # Start button text
        startbuttontext = font.render("START", True, blackish)
        win.blit(startbuttontext, (210, WIN_HEIGHT/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)
        return True

def main(win, clock):
    # posX = random.randint(230, 250)
    # posY = random.randint(100, 500)
    height_pipe = 75
    birds = {0:Bird(POSX1, POSY1, BIRD_IMGS[0]), 1:Bird(POSX2, POSY2, BIRD_IMGS[1])}
    base = Base(630)
    pipes = [Pipe(600, height_pipe)]

    send_msg(server, data_send(PLAYER, 1))

    scores = {0:0, 1:0}
    run = True
    is_move = False
    is_wait = True
    while(run):
        win.fill((0, 0, 0))
        clock.tick(30)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
                pygame.quit()
                quit()
            
            if (event.type == pygame.KEYDOWN):
                if (event.key == KEYJUMP):
                    send_msg(server, data_send(PLAYER, 2))
                    # bird.jump()

        # recv_msg(server)

        #move bird
        for _, bird in birds.items():
            bird.move(is_move)

        rem = []
        add_pipe = False
        for pipe in pipes:
            for _, bird in birds.items():
                if pipe.collide(bird):
                    run = False
                    break
                if (not pipe.passed and 2*pipe.x<bird.x):
                    pipe.passed = True
                    add_pipe = True
                if (pipe.x+pipe.PIPE_TOP.get_width() < 0):
                    rem.append(pipe)
            
            pipe.move(is_move)

        if(PLAYER==0 and add_pipe):
            send_msg(server, data_send(PLAYER, 3))

        socket_list = [server]
        read_socket, write_socket, error_socket = select.select(socket_list, [], [], 0.01)
        for socks in read_socket:
            if socks == server:
                data = recv_msg(socks)
                if(data):
                    plyr = data['Player']
                    #Handle when server broadcast "Start in"
                    if(data["Action"] == 0):
                        is_wait = False
                        draw_wait_room(win, data["Value"])
                    #Handle when server broadcast "Start"
                    elif(data["Action"] == 1):
                        is_move = True
                    #Handle when server broadcast "Jump"
                    elif(data["Action"] == 2):
                        if(plyr in birds):
                            birds[plyr].jump()
                    #Handle when server broadcast "Height Pipe"
                    elif(data["Action"] == 4):
                        height_pipe = data['Value']
                    #Handle when server broadcast "Bird Height"
                    elif(data["Action"] == 5):
                        if(plyr in birds and 
                                abs(birds[plyr].y - data['Value'])>10):
                            draw_window(win, birds, pipes, base, scores, plyr, data['Value'], True)
        
        if(add_pipe):
            for key, _ in birds.items():
                scores[key] += 1
            pipes.append(Pipe(600, height_pipe))
        
        for r in rem:
            pipes.remove(r)
        
        for _, bird in birds.items():
            if (bird.y + bird.img.get_height() >= 630 or bird.y < 0):
                birds = {key:val for key, val in birds.items() if val != bird}
        if len(birds) <=0:
            run = False
        
        # sinc_y_bird += 1
        # if(sinc_y_bird>40):
        #     sinc_y_bird = 0
        #     if(PLAYER in birds):
        #         send_msg(server, data_send(PLAYER, 5, birds[PLAYER].y))

        if(is_wait==True):
            draw_wait_room(win, -2)
        elif(is_move==True):
            draw_window(win, birds, pipes, base, scores)
        base.move(is_move)

    #Handle client sent "End"
    send_msg(server, data_send(PLAYER, -1))

if __name__ == "__main__":
    
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # clock = pygame.time.Clock()
    Thread(target=send_msg, args=(server,data_send(PLAYER, -2))).start()
    Thread(target=recv_msg, args=(server,)).start()

    while True:
        start_menu(win, clock)        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)
    
    server.close()