import threading
import pygame
import socket
import sys
import random

name = "test"

# GLOBAL VARIABLES
bg_x = 0
bg_y = 0
bg_width = 1200
bg_height = 650

bck_x = 500
bck_y = 445
bck_width = 150
bck_height = 209
bck_moved = False

bck_speed = 50
apple_speed = 5
score = 0


def startGame():
    pygame.init()
    screen_size = (1200, 650)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to Bucket Catcher Game in CCN')

    # Colors
    white = (255, 255, 255)
    blue = (0, 102, 204)
    red = (255, 0, 0)

    # Buttons
    start_button = pygame.Rect(450, 250, 300, 80)
    exit_button = pygame.Rect(450, 400, 300, 80)

    font = pygame.font.SysFont(None, 60)

    while True:
        screen.fill(white)

        # Draw Buttons
        pygame.draw.rect(screen, blue, start_button)
        pygame.draw.rect(screen, red, exit_button)

        # Draw Button Text
        start_text = font.render('START', True, (255, 255, 255))
        exit_text = font.render('EXIT', True, (255, 255, 255))
        screen.blit(start_text, (start_button.x + 80, start_button.y + 20))
        screen.blit(exit_text, (exit_button.x + 100, exit_button.y + 20))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return  # START
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


def GameThread():
    global bck_x, bck_y, bck_speed, apple_speed, score

    pygame.init()

    # SET COLORS
    #fontColor = ()
    #shapeColor = (0, 51, 204)
    #shapeColorOver = (255, 0, 204)

    # DISPLAY THE GAME SCREEN
    screen_size = screen_width, screen_height = 1200, 650
    screen = pygame.display.set_mode(screen_size)

    # START A MESSAGE
    pygame.display.set_caption('Welcome to Bucket Catcher Game in CCN')

    #apple = pygame.image.load('apple.png');
    #pygame.display.set_icon(apple)

    # DISPLAY WALLPAPER
    bg_img = pygame.image.load('background.jpg')
    bg = pygame.transform.scale(bg_img, (bg_width, bg_height))

    # DISPLAY BASKET
    bck_img = pygame.image.load('bucket.png')
    bck = pygame.transform.scale(bck_img, (bck_width, bck_height))

    # DISPLAY APPLE
    apple_img = pygame.image.load('apple.png')
    apple_width = 50
    apple_height = 50
    apple = pygame.transform.scale(apple_img, (apple_width, apple_height))

    apple_x = random.randint(0, 1200 - apple_width)  # Falling at a random position
    apple_y = 0

    font = pygame.font.SysFont(None, 50)


    # TICKING CLOCK
    fps = pygame.time.Clock()


    print("GameThread started... ... ...")
    while True:
        screen.fill((255,255,255))
        bg_rect = screen.blit(bg, (bg_x, bg_y))
        bck_rect = screen.blit(bck, (bck_x, bck_y))

        #if bck_moved:
        apple_y += apple_speed
        # apple random falling 1
        apple_rect = screen.blit(apple, (apple_x, apple_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check Collision
        if bck_rect.colliderect(apple_rect):
            print("Caught the apple!")  # Adding score
            score += 1
            apple_x = random.randint(0, 1200 - apple_width)
            apple_y = 0
            apple_speed += 0.2
            bck_speed += 5
        
        if apple_speed > 15:
            apple_speed = 15
        if bck_speed > 500:
            bck_speed = 500

        # Recreate the apple
        if apple_y > bg_height:
            apple_x = random.randint(0, 1200 - apple_width)
            apple_y = 0

        # --------------------
        pygame.draw.rect(screen, (0, 255, 0), bck_rect, 2)  # 버킷 - 초록색 테두리
        pygame.draw.rect(screen, (255, 0, 0), apple_rect, 2)  # 사과 - 빨간색 테두리

        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (20, 20))
        
        pygame.display.update()
        fps.tick(60)


def ServerThread():
    global bck_x, bck_y, bck_speed, apple_speed

    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print("Host: " + str(host))
    port = 5050  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    
    print("ServerThread started... ... ...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            if bck_y - 10 >= 0:  # Block the bucket's movement to avoid out of screen
                bck_y -= bck_speed
                bck_moved = True
        if(data == 's'):
            if bck_y + 10 <= bg_height - bck_height:
                bck_y += bck_speed
                bck_moved = True
        if(data == 'a'):
            if bck_x - 10 >= 0:
                bck_x -= bck_speed
                bck_moved = True
        if(data == 'd'):
            if bck_x + 10 <= bg_width - bck_width:
                bck_x += bck_speed
                bck_moved = True
        

    conn.close()  # close the connection


# t1 = threading.Thread(target=GameThread, args=[])
# t1.start()

if __name__ == '__main__':
    startGame()
    t2 = threading.Thread(target=ServerThread, args=[])
    t2.start()
    pygame.time.wait(100) # Wait for 0.1sec
    GameThread()


