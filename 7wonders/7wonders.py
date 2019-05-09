import os
import pygame
import time
import threading
import queue
       
ThisFolder = os.path.dirname(os.path.realpath(__file__))

screen_width = 800
screen_height = 600

BLACK_COLOUR = (0, 0, 0)
WHITE_COLOUR = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))

background = pygame.Surface(screen.get_size())
background = background.convert()

img1 = pygame.image.load(r'images\Lumber_Yard.png')
img1 = pygame.transform.scale(img1, (img1.get_rect().width//2, img1.get_rect().height//2))
img1 = img1.convert()

clock = pygame.time.Clock()

FPS = 24

bPlaying = True

keymap = {}

img1x, img1y = (0, 0)

bMouseButton1Down = False
bImg1Dragged = False
bImg1Dragged_Prev = False

while bPlaying:
    
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bPlaying = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:          
            print(event.unicode+" DOWN")
            keymap[event.scancode] = event.unicode
        elif event.type == pygame.KEYUP:          
            event.unicode = keymap[event.scancode]
            print(event.unicode+" UP")
    
    # clear screen 
    background.fill(WHITE_COLOUR)
    screen.blit(background, (0, 0))
    
    if pygame.mouse.get_pressed()[0]:
        bMouseButton1Down = True
    else:
        bMouseButton1Down = False   
    
    if bMouseButton1Down and img1.get_rect().move(img1x, img1y).collidepoint(pygame.mouse.get_pos()):
        bImg1Dragged = True
        
    if not bMouseButton1Down:
        bImg1Dragged = False
        
    if bImg1Dragged:
        if (not bImg1Dragged_Prev):
            pygame.mouse.get_rel()
        get_relx, get_rely = pygame.mouse.get_rel()
        img1x += get_relx
        img1y += get_rely
    
    # blit image
    screen.blit(img1,(img1x, img1y))
    
    # display screen
    pygame.display.flip()
    
    bImg1Dragged_Prev = bImg1Dragged
