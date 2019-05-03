#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
006_time_baed_movement.py
url: http://thepythongamebook.com/en:part2:pygame:step006
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with python3.4 and pyhton2.7
 
bouncing ball. Movement is now time based.
Because at coding, you never know exactly how many milliseconds
will have been passed between two frames, this example use pygame's
clock function to calculate the passed time and move the surface at
constantly the same speed. 
If you toggle the wild circle painting by pressing SPACE, the computer
has more to paint, framerate will drop, more time will pass between 
2 frames and movement of the ball surface will be choppy (less smooth).
However, the movent speed remain unchanged because of the time-based movement.
"""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division
import pygame
import random

def T_Option(x, screen_width):
    return 1-0.0001*(x/screen_width)**2
def T_Prime(x, screen_width):
    return 0.99-0.00005*(x/screen_width)**2
def T_Backup(x, screen_width):
    return 0.98-0.000025*(x/screen_width)**2
Degradation = {
    0 : { "FUNCTION" : T_Option, "NAME": "Option"},
    1 : { "FUNCTION" : T_Prime,  "NAME": "Prime"},
    2 : { "FUNCTION" : T_Backup, "NAME": "Backup"},
}
CarColourList = [
    (0,210,190    ), # Mercedes
    (220,0,0      ), # Ferrari
    (0,50,125     ), # Red Bull
    (90,90,90     ), # Haas
    (255,245,0    ), # Renault
    (245,150,200  ), # Force India
    (0,50,255     ), # Torro Rosso
    (255,135,0    ), # McLaren
    (155,0,0      ), # Sauber
    (255,255,255  ), # Williams
]
CarNameList = [
    'HAM',
    'BOT',
    'VET',
    'RAI',
    'RIC',
    'VER',
    'MAG',
    'GRO',
    'HUL',
    'SAI',
    'OCO',
    'PER',
    'GAS',
    'HAR',
    'ALO',
    'VAN',
    'LEC',
    'ERI',
    'STR',
    'SIR',
]
    
class Car:

    def __init__(self, screen, x, pace, tyre = 0, colour = None, blity = 0, name = 'REX'):
           
        self.screen = screen
        self.screen_width = screen.get_rect().width
        self.colour = colour        
        self.surface = self.init_surface()
        self.surface_width = self.surface.get_rect().width
        self.x = x
        self.pace = pace
        self.dx = pace
        self.tyre = tyre
        self.blity = blity
        self.name = name
        self.diff = 0

    def init_surface(self):
        width = 20
        height = 20
        surface = pygame.Surface((width, height))
        surface.set_colorkey((0,0,0))
        #pygame.draw.circle(Surface, color, pos, radius, width=0)
        pygame.draw.rect(
            surface,
            self.colour,
            (0, 0, width, height),
        )
        return surface.convert_alpha()        # for faster blitting. because transparency, use convert_alpha()       

    def calc_dx(self, prev_car):
        degr = Degradation[self.tyre]["FUNCTION"](self.x, self.screen_width)
        slip = self.calc_slip(prev_car)
        self.dx = self.slip * degr * self.pace         
        
    def calc_x(self, seconds):
        warp = 6
        self.x += self.dx * warp * seconds       

    def calc_diff(self, prev_car):
        self.diff = (prev_car.x - self.x)/self.dx        
    
    def calc_slip(self, prev_car):
        slipx = 10*car_length
        slipv = 1.0025
        if (prev_car.x - self.x) < slipx:
            if (prev_car.x - self.x) > slipx/2:
                self.slip = (1-slipv)/slipx*(prev_car.x - self.x)+slipv
            else:
                self.slip = (slipv-1)/slipx*(prev_car.x - self.x)+1
        else:
            self.slip = 1
    
    def blit(self):
        surface_width = self.surface_width
        screen_width = self.screen_width
       
        blitx = round(self.x)%screen_width-round(surface_width/2)
        blity = self.blity
        
        self.screen.blit(self.surface, (blitx, blity))     
        if blitx < 0:
            self.screen.blit(self.surface, (blitx + screen_width, blity))
        if screen_width - blitx < surface_width: 
            self.screen.blit(self.surface, (blitx - screen_width, blity))        

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
screen = pygame.display.set_mode((1024, 400)) # try out larger values and see what happens !
screen_width = screen.get_rect().width
background = pygame.Surface(screen.get_size()) #create surface for background
background.fill((0,0,0))     #fill the background white (red,green,blue)
background = background.convert()  #convert surface for faster blitting
mycar_list = []
screen.blit(background, (0,0))     #blit the background on screen (overwriting all)
nmb_of_cars = 20
best_lap_time = 80 # seconds
grid_interval = 1.38e-03*screen_width
car_length = 1e-03*screen_width
for i in range(nmb_of_cars):
    mycar = Car(
        screen = screen,
        x = grid_interval*(-1-i),
        pace = 1*screen_width*0.998478**i/best_lap_time,
        tyre = random.randint(0, 2),
        # tyre = 1,
        colour = CarColourList[int(i/2)],
        blity = i*20,
        name = CarNameList[i],
    )
    mycar.blit()    
    mycar_list.append(mycar)
 
clock = pygame.time.Clock()        #create pygame clock object
bRacing = True
FPS = 60                           # desired max. framerate in frames per second. 
playtime = 0
font = pygame.font.SysFont('mono', 20, bold = True)
 
while bRacing:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    playtime += seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bRacing = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                bRacing = False # user pressed ESC
            elif event.key == pygame.K_1: 
                FPS = 10
            elif event.key == pygame.K_2:
                FPS = 20
            elif event.key == pygame.K_3:
                FPS = 30
            elif event.key == pygame.K_4:
                FPS = 40
            elif event.key == pygame.K_5:
                FPS = 50
            elif event.key == pygame.K_6:
                FPS = 60
            elif event.key == pygame.K_7:
                FPS = 70
            elif event.key == pygame.K_8:
                FPS = 80
            elif event.key == pygame.K_9:
                FPS = 90
            elif event.key == pygame.K_0:
                FPS = 1000 # absurd high value
 
    screen.blit(background, (0,0))     #draw background on screen (overwriting all)
      
    sorted_mycar_list = sorted(
        mycar_list,
        key = lambda mycar: mycar.x,
        reverse = True,
    )

    prev_car = sorted_mycar_list[0]
    for mycar in sorted_mycar_list: 
        mycar.calc_dx(prev_car)
        prev_car = mycar

    prev_car = sorted_mycar_list[0]    
    for mycar_index, mycar in enumerate(sorted_mycar_list): 
        mycar.calc_x(seconds)
        mycar.calc_diff(prev_car)
        
        mycar.blity = mycar_index*20
        mycar.blit()
        text = '{} {:+.2f} {}'.format(mycar.name, mycar.diff, Degradation[mycar.tyre]["NAME"])
        surface = font.render(text, True, mycar.colour)
        screen.blit(surface, (0, mycar.blity))

        prev_car = mycar        
 
    lap = int(sorted_mycar_list[0].x/screen_width)+1
    pygame.display.set_caption("limit FPS to {} (now: {:.2f}). Lap {}".format(FPS, clock.get_fps(), lap))
       
    pygame.display.flip()
    
print("This 'game' was played for {:.2f} seconds".format(playtime))