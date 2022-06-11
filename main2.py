import sys
from numpy import NaN
import pygame
import os
import socket
import select
import sys
import pickle
from threading import Thread
from datetime import date
import time

PLAYER = 1
KEYJUMP = pygame.K_UP

sys.path.append('/object_game/')
pygame.init()

from object_game.pipe import Pipe
from object_game.bird import Bird
from object_game.base import Base

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip_address = '127.0.0.1'
# port = 8081
ip_address = '13.229.230.226'
port = 5555
server.connect((ip_address, port))

POSX1 = 235
POSY1 = 200
POSX2 = 245
POSY2 = 400
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
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

# Function to create a button
def create_button(x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    # Mouse get pressed can run without an integer, but needs a 3 or 5 to indicate how many buttons
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(win, hovercolor, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(win, defaultcolor, (x, y, width, height))


# Start menu returns true until we click the Start button
def start_menu():
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
        start_button = create_button(200, WIN_HEIGHT/2 - 8 , 120, 40, lightgrey, slategrey)

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


def data_send(player, act, val=None):
    data_dict = {"Player":player, "Action":act, "Value":val}
    data = pickle.dumps(data_dict)
    return data

def send_msg(sock, data):
    sock.send(data)
    # sys.stdout.write(data)
    sys.stdout.flush()

def recv_msg(sock):
    try:
        data = sock.recv(2048)
        data_pick = pickle.loads(data)
        print(data_pick)
        return data_pick
    except:
        # print("Exception Occured!")
        pass

def draw_window(win, birds, pipes, base, scores, player=PLAYER, sinc_height=0, sinc_height_status=False):
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

def main(win, clock):

    # posX = random.randint(230, 250)
    # posY = random.randint(100, 500)
    height_pipe = 75
    birds = {0:Bird(POSX1, POSY1, BIRD_IMGS[0]), 1:Bird(POSX2, POSY2, BIRD_IMGS[1])}
    base = Base(630)
    pipes = [Pipe(600, height_pipe)]
    
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # clock = pygame.time.Clock()

    send_msg(server, data_send(PLAYER, 1))

    scores = {0:0, 1:0}

    run = True
    is_move = False
    is_wait = True
    sinc_y_bird = 0
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
                if (not pipe.passed and pipe.x<bird.x):
                    pipe.passed = True
                    add_pipe = True
                if (pipe.x+pipe.PIPE_TOP.get_width() < 0):
                    rem.append(pipe)
            
            pipe.move(is_move)

        # if(add_pipe):
        #     send_msg(server, data_send(PLAYER, 3))

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
        
        if (add_pipe):
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
        
    
    send_msg(server, data_send(PLAYER, -1))

if __name__ == "__main__":
    
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # clock = pygame.time.Clock()
    Thread(target=send_msg, args=(server,data_send(PLAYER, -2))).start()
    Thread(target=recv_msg, args=(server,)).start()

    # start_menu()

    while True:
        
        start_menu()

        # Thread(target=send_msg, args=(server,data_send(PLAYER, "Init Thread"))).start()
        # Thread(target=recv_msg, args=(server,)).start()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)
    
    server.close()

    # main(win,clock)

    # menu = pygame_menu.Menu('Welcome', 400, 300,
    #                     theme=pygame_menu.themes.THEME_BLUE)

    # menu.add.text_input('Name :', default='Player')
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
    # menu.add.button('Play', main(win,clock))
    # menu.add.button('Quit', pygame_menu.events.EXIT)

    # menu.mainloop(win)

    # main()