import os
import time
import threading
import queue
import sys
import pandas
import pprint
import copy
import random
       
ThisFolder = os.path.dirname(os.path.realpath(__file__))

class Wonder(object):
    def __init__(self, info_df):
        self.info_df = info_df
        self.cards_L = []
        # -- wonder stages
        stage_count = 2
        if not pandas.isna(info_df['stage3_cost']):
            stage_count = 3
        if not pandas.isna(info_df['stage4_cost']):
            stage_count = 4
        self.stage_count = stage_count
        self.stages_L = []

class Player(object):
    def __init__(self, wonder, cards_L):
        self.wonder = wonder
        self.cards_L = cards_L
        self.money = 3
    def build_structure(self, card):
        self.cards_L.remove(card)
        self.wonder.cards_L.append(card)
    def build_wonder(self, card):
        self.cards_L.remove(card)
        self.wonder.stages_L.append(card)

p_T = ("3p", "4p", "5p", "6p", "7p",)

stc_df = pandas.read_csv(os.path.join(ThisFolder, 'structures.csv'))
wdr_df = pandas.read_csv(os.path.join(ThisFolder, 'wonders.csv'))

empty_decks_D = {
    "3p" : [],
    "4p" : [],
    "5p" : [],
    "6p" : [],
    "7p" : [],
}

# ---- PARTIAL DECKS AS LIST OF DICTIONARIES
age1_partial_decks_D = copy.deepcopy(empty_decks_D)
age2_partial_decks_D = copy.deepcopy(empty_decks_D)
age3_partial_decks_D = copy.deepcopy(empty_decks_D)
guilds_deck = []

for row_ in stc_df.iterrows():
    
    row_index = row_[0]
    row = row_[1]

    stc_D = {}
    for col in row.keys():
        stc_D[col] = row[col]
        
    if row["age"] == "I":
        for p_S in p_T:    
            if row[p_S] == 1:
                age1_partial_decks_D[p_S].append(stc_D)
    elif row["age"] == "II":
        for p_S in p_T:    
            if row[p_S] == 1:
                age2_partial_decks_D[p_S].append(stc_D)
    elif row["age"] == "III":
        for p_S in p_T:    
            if row[p_S] == 1:
                age3_partial_decks_D[p_S].append(stc_D)
        if row["type"] == "Guild":
            guilds_deck.append(stc_D) 

# ---- AGE I : DECKS AS LIST OF DICTIONARIES
age1_decks_D = {}
age1_decks_D["3p"] = copy.deepcopy(age1_partial_decks_D["3p"])
age1_decks_D["4p"] = age1_decks_D["3p"] + age1_partial_decks_D["4p"]
age1_decks_D["5p"] = age1_decks_D["4p"] + age1_partial_decks_D["5p"]
age1_decks_D["6p"] = age1_decks_D["5p"] + age1_partial_decks_D["6p"]
age1_decks_D["7p"] = age1_decks_D["6p"] + age1_partial_decks_D["7p"]

# ---- AGE II : DECKS AS LIST OF DICTIONARIES
age2_decks_D = {}
age2_decks_D["3p"] = copy.deepcopy(age2_partial_decks_D["3p"])
age2_decks_D["4p"] = age2_decks_D["3p"] + age2_partial_decks_D["4p"]
age2_decks_D["5p"] = age2_decks_D["4p"] + age2_partial_decks_D["5p"]
age2_decks_D["6p"] = age2_decks_D["5p"] + age2_partial_decks_D["6p"]
age2_decks_D["7p"] = age2_decks_D["6p"] + age2_partial_decks_D["7p"]

# ---- AGE III : DECKS AS LIST OF DICTIONARIES
age3_decks_D = {}
age3_decks_D["3p"] = copy.deepcopy(age3_partial_decks_D["3p"])
age3_decks_D["4p"] = age3_decks_D["3p"] + age3_partial_decks_D["4p"]
age3_decks_D["5p"] = age3_decks_D["4p"] + age3_partial_decks_D["5p"]
age3_decks_D["6p"] = age3_decks_D["5p"] + age3_partial_decks_D["6p"]
age3_decks_D["7p"] = age3_decks_D["6p"] + age3_partial_decks_D["7p"]

# --- SHUFFLE GUILDS
random.shuffle(guilds_deck)

# --- SELECT GUILDS AND ADD THEM TO AGE III DECKS
g_D = {
    "3p" : 5,
    "4p" : 6,
    "5p" : 7,
    "6p" : 8,
    "7p" : 9,
}
for p_S in p_T:
    age3_decks_D[p_S] += guilds_deck[0:g_D[p_S]]

# ---- DECKS AS PANDAS DATAFRAMES
age1_decks_df_D = {}
age2_decks_df_D = {}
age3_decks_df_D = {}
for p_S in p_T:
    age1_decks_df_D[p_S] = pandas.DataFrame(age1_decks_D[p_S])
    age2_decks_df_D[p_S] = pandas.DataFrame(age2_decks_D[p_S])
    age3_decks_df_D[p_S] = pandas.DataFrame(age3_decks_D[p_S])

# ---- HOW MANY PLAYERS
how_many_players = "4p"

# ---- CHOOSE RIGHT DECKS
age1_deck_df = age1_decks_df_D[how_many_players]
age2_deck_df = age2_decks_df_D[how_many_players]
age3_deck_df = age3_decks_df_D[how_many_players]

player_count = len(age1_deck_df)//7

# ---- WONDERS
wonder_indexes_L = list(range(7))
random.shuffle(wonder_indexes_L)
player_wonders_L = []
for wonder_index in wonder_indexes_L[:player_count]:
    player_wonders_L.append(Wonder(wdr_df.iloc[wonder_index]))

# ---- LIST OF CARD INDEXES
age1_cards_L = list(range(len(age1_deck_df)))
age2_cards_L = list(range(len(age2_deck_df)))
age3_cards_L = list(range(len(age3_deck_df)))
random.shuffle(age1_cards_L)
random.shuffle(age2_cards_L)
random.shuffle(age3_cards_L)

# ---- DISTRIBUTE CARDS
player_hands_L = []
for p in range(player_count):
    player_hands_L.append([])
for card_index, card in enumerate(age1_cards_L):
    player_hands_L[(card_index)%player_count].append(card)

# ---- PLAYERS
players_L = []
for p in range(player_count):
    players_L.append(
        Player(
            wonder = Wonder(wdr_df.iloc[wonder_indexes_L[:player_count][p]]),
            cards_L = player_hands_L[p],
        )
    )
    
print(players_L[0].cards_L)
print(players_L[0].wonder.stages_L)
players_L[0].build_wonder(players_L[0].cards_L[0])
print(players_L[0].cards_L)
print(players_L[0].wonder.stages_L)
    
sys.exit()

import pygame

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
