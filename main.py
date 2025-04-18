import pygame
import keyboard
import sys
import threading
import time


pygame.init()

# SET COLORS
fontColor = ()
shapeColor = (0, 51, 204)
shapeColorOver = (255, 0, 204)

# DISPLAY THE GAME SCREEN
screen_size = screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode(screen_size)

# START A MESSAGE
pygame.display.set_caption('Welcome to Bucket Catcher Game in CCN')


# DISPLAY IMAGES
basket = pygame.image.load('bsck.png')
pygame.display.set_icon(basket)
bg_img = pygame.image.load('bg.jpg')

# TICKING CLOCK
fps = pygame.time.Clock()


print("GameThread started... ... ...")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #screen.blit(bg_img, (0, 0))
    pygame.display.update()

    fps.tick(60)



'''
    rect2 = pygame.Rect(0, 0, 75, 75)
    rect1 = pygame.Rect(0, 0, 25, 25)
    
    
    colorRect = (shapeColor)
    colorRect2 = (shapeColorOver)
    global posx 
    global posy
    
        rect1.center = (posx, posy)
        collision = rect1.colliderect(rect2)
        pygame.draw.rect(screen, colorRect, rect1)
        if collision:
            pygame.draw.rect(screen, colorRect2, rect2, 6, 1)
        else:
            pygame.draw.rect(screen, colorRect, rect2, 6, 1)
'''


pygame.quit()
