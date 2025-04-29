import threading
import pygame
import socket
import sys
import random

name = "test"

# GLOBAL VARIABLES
# background image
bg_x = 0
bg_y = 0
bg_width = 1200
bg_height = 650

# bucket
bck_x = 500
bck_y = 445
bck_width = 150
bck_height = 209
bck_moved = False

# speed & score
bck_speed = 50
apple_speed = 3
score = 0


def startGame():
    pygame.init()
    screen_size = (1200, 650)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to Bucket Catcher!')

    background_color = (255, 204, 153)

    start_button = pygame.Rect(350, 500, 200, 70)
    exit_button = pygame.Rect(650, 500, 200, 70)

    title_font = pygame.font.SysFont(None, 100)
    button_font = pygame.font.SysFont(None, 50)

    button_color = (255, 178, 102)
    button_hover_color = (255, 140, 26)
    font_color = (80, 40, 0)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(background_color)

        # Game Title
        title_text = title_font.render('Bucket Catcher', True, font_color)
        title_rect = title_text.get_rect(center=(screen_size[0] // 2, 200))
        screen.blit(title_text, title_rect)

        # Buttons
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, start_button, border_radius=10)
        else:
            pygame.draw.rect(screen, button_color, start_button, border_radius=10)

        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, exit_button, border_radius=10)
        else:
            pygame.draw.rect(screen, button_color, exit_button, border_radius=10)

        # Decorate Buttons
        start_text = button_font.render(' START ', True, font_color)
        start_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_rect)
        exit_text = button_font.render(' EXIT ', True, font_color)
        exit_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def gameOver(screen, font, score):
    background_color = (255, 204, 153)
    font_color = (80, 40, 0)

    screen.fill(background_color)

    # Fonts
    header1_font = pygame.font.SysFont(None, 100)
    header3_font = pygame.font.SysFont(None, 60)

    # Rendering texts
    gameOver_text = header1_font.render('GAME OVER', True, font_color)
    score_text = header3_font.render(f'Final Score: {score}', True, font_color)

    screen_width, screen_height = screen.get_size()
    gameOver_rect = gameOver_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    screen.blit(gameOver_text, gameOver_rect)
    screen.blit(score_text, score_rect)

    pygame.display.update()
    pygame.time.wait(3000)  # Wait for 3 secs
    pygame.quit()
    sys.exit()


def GameThread():
    global bck_x, bck_y, bck_speed, apple_speed, score

    pygame.init()

    screen_size = screen_width, screen_height = 1200, 650
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to Bucket Catcher!')

    bg_img = pygame.image.load('background.jpg')
    bg = pygame.transform.scale(bg_img, (bg_width, bg_height))

    bck_img = pygame.image.load('bucket.png')
    bck = pygame.transform.scale(bck_img, (bck_width, bck_height))
    
    apple_img = pygame.image.load('apple.png')
    apple_width = 50
    apple_height = 50
    apple = pygame.transform.scale(apple_img, (apple_width, apple_height))

    apple_x = random.randint(0, 1200 - apple_width)
    apple_y = 0

    font = pygame.font.SysFont(None, 50)
    fps = pygame.time.Clock()

    frame_counter = 0
    apple_falling = False

    print("GameThread started...")
    while True:
        screen.fill((255,255,255))
        screen.blit(bg, (bg_x, bg_y))
        bck_rect = screen.blit(bck, (bck_x, bck_y))
        apple_rect = screen.blit(apple, (apple_x, apple_y))

        # Increase the speed of falling apple
        if apple_falling:
            apple_y += apple_speed

        # If missing an apple -> game over
        if apple_y > bg_height:
            print("Game Over!")
            gameOver(screen, font, score)
            return

        # Detect Collision of the bucket and the apple
        if bck_rect.colliderect(apple_rect):
            print("Caught the apple!")
            score += 1
            apple_x = random.randint(0, 1200 - apple_width)
            apple_y = 0
            apple_speed += 0.2
            bck_speed += 5

        # Delay in the beginning (before apple_falling)
        if not apple_falling:
            frame_counter += 1
            if frame_counter >= 360:  # Wait for 6 secs
                apple_falling = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Limit the max-speed
        if apple_speed > 50:
            apple_speed = 50
        if bck_speed > 500:
            bck_speed = 500

        # Score
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
            if bck_y + 10 <= (bg_height - bck_height):
                bck_y += bck_speed
                bck_moved = True
        if(data == 'a'):
            if bck_x - 10 >= 0:
                bck_x -= bck_speed
                bck_moved = True
        if(data == 'd'):
            if bck_x + 10 <= (bg_width - bck_width):
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


