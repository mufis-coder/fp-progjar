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
PLAYER = "Player2"
KEYJUMP = pygame.K_UP

POSX1 = 235
POSY1 = 200
POSX2 = 245
POSY2 = 400
WIN_WIDTH = 500
WIN_HEIGHT = 700
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

BIRD_1OR2 = {"Player1":0, "Player2":1}

def data_send(player, msg):
    data_dict = {player: msg}
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

    birds = [Bird(POSX1, POSY1, BIRD_IMGS), Bird(POSX2, POSY2, BIRD_IMGS)]
    base = Base(630)
    pipes = [Pipe(600)]
    
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # clock = pygame.time.Clock()

    score = 0
    
    run = True
    is_move = False
    while(run):
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

        socket_list = [server]
        read_socket, write_socket, error_socket = select.select(socket_list, [], [], 0.01)
        for socks in read_socket:
            if socks == server:
                data = recv_msg(socks)
                if(PLAYER in data and data[PLAYER] == 'Start'):
                    is_move = True
                elif(PLAYER in data and data[PLAYER] == 'Jump'):
                    birds[BIRD_1OR2[PLAYER]].jump()

        
        #move bird
        for bird in birds:
            bird.move(is_move)

        add_pipe = False
        rem = []
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
        
        if (add_pipe):
            score += 1
            pipes.append(Pipe(600))
        
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
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    Thread(target=send_msg, args=(server,data_send(PLAYER, "Init Thread"))).start()
    Thread(target=recv_msg, args=(server,)).start()

    main(win,clock)

    # menu = pygame_menu.Menu('Welcome', 400, 300,
    #                     theme=pygame_menu.themes.THEME_BLUE)

    # menu.add.text_input('Name :', default='Player')
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
    # menu.add.button('Play', main(win,clock))
    # menu.add.button('Quit', pygame_menu.events.EXIT)

    # menu.mainloop(win)

    # main()