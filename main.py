import sys
from numpy import NaN
import pygame
import os
import random
import pygame_menu
import socket
import select
import sys
import pickle
from threading import Thread
from datetime import date

sys.path.append('/object_game/')
pygame.init()

from object_game.pipe import Pipe
from object_game.bird import Bird
from object_game.base import Base

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
			pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), 
			pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PLAYER = "Player1"
KEYJUMP = pygame.K_SPACE

POSX1 = 235
POSY1 = 200
POSX2 = 245
POSY2 = 400
WIN_WIDTH = 500
WIN_HEIGHT = 700
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

BIRD_1OR2 = {"Player1":0, "Player2":1}

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

def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()

def main(win, clock):

    # posX = random.randint(230, 250)
    # posY = random.randint(100, 500)
    height_pipe = 75
    birds = [Bird(POSX1, POSY1, BIRD_IMGS), Bird(POSX2, POSY2, BIRD_IMGS)]
    base = Base(630)
    pipes = [Pipe(600, height_pipe)]
    
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # clock = pygame.time.Clock()

    score = 0
    
    run = True
    is_move = False
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
                    send_msg(server, data_send(PLAYER, "Jump"))
                    # bird.jump()

        # recv_msg(server)

        #move bird
        for bird in birds:
            bird.move(is_move)

        rem = []
        add_pipe = False
        for pipe in pipes:
            for bird in birds:
                if pipe.collide(bird):
                    run = False
                    break
                if (not pipe.passed and pipe.x<bird.x):
                    pipe.passed = True
                    add_pipe = True
                if (pipe.x+pipe.PIPE_TOP.get_width() < 0):
                    rem.append(pipe)
            
            pipe.move(is_move)

        if(add_pipe):
            send_msg(server, data_send(PLAYER, "Add Pipe"))

        socket_list = [server]
        read_socket, write_socket, error_socket = select.select(socket_list, [], [], 0.01)
        for socks in read_socket:
            if socks == server:
                data = recv_msg(socks)
                plyr = data['Player']
                if(data["Action"] == 'Start'):
                    is_move = True
                elif(data["Action"] == 'Jump'):
                    birds[BIRD_1OR2[plyr]].jump()
                elif(data["Action"] == "Height Pipe"):
                    height_pipe = data['Value']
        
        if (add_pipe):
            score += 1
            pipes.append(Pipe(600, height_pipe))
        
        for r in rem:
            pipes.remove(r)
        
        for bird in birds:
            if (bird.y + bird.img.get_height() >= 630 or bird.y < 0):
                birds.remove(bird)
        if len(birds) <=0:
            run = False
        
        base.move(is_move)
        draw_window(win, birds, pipes, base, score)
    
    print("End Game")
    send_msg(server, data_send(PLAYER, "End"))
    server.close()

if __name__ == "__main__":
    
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # clock = pygame.time.Clock()
    Thread(target=send_msg, args=(server,data_send(PLAYER, "Init Thread"))).start()
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

    # main(win,clock)

    # menu = pygame_menu.Menu('Welcome', 400, 300,
    #                     theme=pygame_menu.themes.THEME_BLUE)

    # menu.add.text_input('Name :', default='Player')
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
    # menu.add.button('Play', main(win,clock))
    # menu.add.button('Quit', pygame_menu.events.EXIT)

    # menu.mainloop(win)

    # main()