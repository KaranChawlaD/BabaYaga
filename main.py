from email.mime import image
import pygame
import random
from pygame.locals import *
from pygame import mixer

pygame.init()
mixer.init()

# Test

#Pygame Window Name
pygame.display.set_caption('Baba Yaga')

#Stored Colours
ORANGE = (255, 174, 66)
BLACK = (0, 0, 0)

#Screen Dimensions
WIDTH, HEIGHT = 900, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

#Game Clock
CLOCK = pygame.time.Clock()

#Images in Game
BABY_YODA = pygame.image.load('Baby Yoda.jpg')
LIGHTSABER = pygame.image.load('Lightsaber.png')
HEART = pygame.image.load('Heart.png')
pygame.mixer.music.load("Theme.wav")
pygame.mixer.music.play()
NEW_BABY_YODA = pygame.transform.rotozoom(BABY_YODA, 0.0, 0.075)
NEW_LIGHTSABER = pygame.transform.rotozoom(LIGHTSABER, 0.0, 0.075)
NEW_HEART = pygame.transform.rotozoom(HEART, 0.0, 0.075)
#Stored Font
FONT_SANS = pygame.font.Font('freesansbold.ttf', 30)

#Set Icon
pygame.display.set_icon(BABY_YODA)

#Initializing Baby Yoda as a Rectangle
RECT_BABY_YODA = NEW_BABY_YODA.get_rect()
RECT_BABY_YODA.center = 25, 100   

#Used Variables
RAND_SPAWN = 0
TIME = 0
TEMP_TIME = 0

#Time Tracking Variables
RUNNING = True
GAMEOVER = False
HACK = False
HIT_LIGHTSABER = False
HIT_HEART = False
DISSAPEARHEART = False

#Random Lightsaber/Heart Coordinate Array
LIGHTSABER_X_COOR=[0, 0, 0, 0, 0, 0, 0, 0]
HEART_X_COOR = random.randint(200, 850)
HEART_Y_COOR = (random.randint(100, 799)//100) * 100 + 75
HEART_COUNTER = 3

def RANDOM_BABY_YODA_PLACEMENT(): 
    RAND_SPAWN = random.randint(100, 899)//100 * 100
    RECT_BABY_YODA.center = 25, RAND_SPAWN
    for i in range(len(LIGHTSABER_X_COOR)):
        LIGHTSABER_X_COOR[i] = random.randint(200, 850)
    
    
RANDOM_BABY_YODA_PLACEMENT()

while RUNNING:

    SCREEN.fill(ORANGE) #Setting Background of Game

    #Game Borders
    pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 900, 50))
    pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 850, 900, 50))

    #Event Sequences
    for event in pygame.event.get():
        
        if event.type == QUIT: #If Press Quit, Then Shut Down Window
            RUNNING = False
        
        elif event.type == pygame.KEYDOWN and GAMEOVER==False: #If a Key is Pressed During a Live Game
            if event.key == pygame.K_UP: #If the UP Key is Pressed

                if 100 < RECT_BABY_YODA.center[1]: 
                    RECT_BABY_YODA.move_ip(0, -100) #Moving UP if There's Space to Move UP

            if event.key == pygame.K_DOWN: #If the DOWN Key is Pressed

                if RECT_BABY_YODA.center[1] < 800:
                    RECT_BABY_YODA.move_ip(0, 100) #Moving DOWN if There's Space to Move DOWN

            if event.key == pygame.K_LCTRL:
                HACK = True

            if event.key == pygame.K_LSHIFT:
                HACK = False
                
        elif event.type == pygame.KEYDOWN and GAMEOVER==True: #If a Key is Pressed During a Finished Game
            if event.key == pygame.K_SPACE: #Resetting the Game

                RECT_BABY_YODA.center = 25, 100 #Resetting Image
                TIME = CLOCK.tick() 
                TIME = 0 #Resetting Timer
                HEART_COUNTER = 3
                HIT_LIGHTSABER = False
                HIT_HEART = False
                DISSAPEARHEART = False
                RANDOM_BABY_YODA_PLACEMENT()
                GAMEOVER = False #Resseting GAMEOVER Bool

    if not GAMEOVER:
        TIME = round(TIME + CLOCK.tick()/1000, 2)

        if RECT_BABY_YODA.center[0] < 875:

            RECT_BABY_YODA.move_ip((TIME//10 + 1), 0)
            pygame.time.wait(5)

        if RECT_BABY_YODA.center[0] >= 875:
            HIT_LIGHTSABER = False
            HIT_HEART = False
            DISSAPEARHEART = False
            RANDOM_BABY_YODA_PLACEMENT()
            HEART_X_COOR = random.randint(200, 850)
            HEART_Y_COOR = random.randint(100, 799)//100 *100 - 25

        for k in range(8):
            if NEW_BABY_YODA.get_rect(topleft = (RECT_BABY_YODA.center[0] - 32.5, RECT_BABY_YODA.center[1] - 32)).colliderect(NEW_LIGHTSABER.get_rect(topleft = (LIGHTSABER_X_COOR[k], k*100+70))) and HACK == False:
                if not HIT_LIGHTSABER: 
                    HIT_LIGHTSABER = True
                    DISSAPEARHEART = True
                    HEART_COUNTER -= 1

    if NEW_BABY_YODA.get_rect(topleft = (RECT_BABY_YODA.center[0] - 32.5, RECT_BABY_YODA.center[1] - 32)).colliderect(NEW_HEART.get_rect(topleft = (HEART_X_COOR, HEART_Y_COOR))):
        if HEART_COUNTER < 3 and HIT_HEART == False and HIT_LIGHTSABER == False:
            HEART_COUNTER += 1
            DISSAPEARHEART = True
        HIT_HEART = True
        
    if HEART_COUNTER == 0:
        GAMEOVER = True

    if GAMEOVER:
        SCREEN.blit(FONT_SANS.render("game over", True, (255, 255, 255)), (600, 862.5))
        SCREEN.blit(FONT_SANS.render("press 'space' to restart game", True, (255, 255, 255)), (0, 862.5))

    for p in range (8):
        SCREEN.blit(NEW_LIGHTSABER, (LIGHTSABER_X_COOR[p], p*100+70))
    if not DISSAPEARHEART:
        SCREEN.blit(NEW_HEART, (HEART_X_COOR, HEART_Y_COOR))
        
    for l in range (9):
        pygame.draw.line(SCREEN, (0, 0, 0), (0, l*100+50), (900, l*100+50), 3)

    SCREEN.blit(NEW_BABY_YODA, RECT_BABY_YODA)

    SCREEN.blit(FONT_SANS.render(str(TIME), True, (255, 255, 255)), (800, 862.5))
    SCREEN.blit(FONT_SANS.render("WORLD RECORD IS 81.28 seconds", True, (255, 255, 255)), (0, 10))

    
    if HEART_COUNTER == 3:
        SCREEN.blit(NEW_HEART, (850, 0))
        SCREEN.blit(NEW_HEART, (800, 0))
        SCREEN.blit(NEW_HEART, (750, 0))
    if HEART_COUNTER == 2:
        SCREEN.blit(NEW_HEART, (850, 0))
        SCREEN.blit(NEW_HEART, (800, 0))  
    if HEART_COUNTER == 1:
        SCREEN.blit(NEW_HEART, (850, 0))     


    pygame.draw.rect(SCREEN, BLACK, RECT_BABY_YODA, 2)
 
    pygame.display.update()

pygame.quit()
