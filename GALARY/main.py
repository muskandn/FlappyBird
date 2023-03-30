import random
import sys#for existing from the game
import pygame
import os
print(os.getcwd())
#os.chdir('C:/Users/DELL/Desktop/Flappy bird/GALARY')

from pygame.locals import *
#global variables for the game
FPS=32#frame per second
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))##initiallizing
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
#GAME_SOUNDS={}
PLAYER='GALARY/sprites/bird.png.png'
BACKGROUND='GALARY/sprites/background.png.png'
PIPE='GALARY/sprites/pipe.png.png'

def welcomeScreen():
    
    '''shows weicome images on the screen'''

    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT- GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENHEIGHT- GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get():##shows the button clicked on the keyboard
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if the user preses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return 

            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))    
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))    
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))    
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    
    #create 2 pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()

    #my list of upper pipes
    upperPipes=[{'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2,'y':newPipe2[0]['y']}]

    #my list of lower pipes
    lowerPipes=[{'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2,'y':newPipe2[1]['y']}]

    pipeVelX=-4
    
    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=-1

    playerFlapAccv=-8 #velocity while flapping
    playerFlapped=False #it is true i=only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if the user preses space or up key, start the game for them
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP): 
                if playery>0:
                    playerVelY=playerFlapAccv
                    playerFlapped=True
                    #GAME_SOUNDS['wing'].play()

        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)#this function will return true of the player is crashed
        if crashTest:
            return

        #check for score
        playerMidPos=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<=playerMidPos<pipeMidPos+4:
                score+=1
                print(f"your score is {score}")
                #GAME_SOUNDS['point'].play()

        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+=playerAccY   

        if playerFlapped:
            playerFlapped=False
        playerHeight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playerVelY,GROUNDY-playery-playerHeight) ##video no 122 in 1:29:40  

        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX
            lowerPipe['x']+=pipeVelX###pipe moves in forward direction....as velocity is negitive here
        
        #add a new pipe when the first is about to cross the left most part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        ##if the pipes are out of the screen....
        if upperPipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)    
            lowerPipes.pop(0)    

        #lets blits our sprites new
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(0,GROUNDY))#?????????????????????????????????????????????????????????ERROR
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))


        mydigits=[int(x) for x in list(str(score))]
        width=0
        for digit in mydigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()

        Xoffset=(SCREENWIDTH-width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update() 
        FPSCLOCK.tick(FPS) 
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery>GROUNDY-25 or playery<0:
        #GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight=GAME_SPRITES['pipe'][0].get_height()
        if(playery<pipeHeight+pipe['y'] and abs(playerx - pipe['x']) <GAME_SPRITES['pipe'][0].get_width()):#abs is almost equal to absolute value.....
            return True
        
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height()>pipe['y']) and abs(playerx - pipe['x']) <GAME_SPRITES['pipe'][0].get_width():
            return True





def getRandomPipe():
    """generate positions of two pipes(two pipe one bottom straight and one one top rotated) for bliting on the screen"""
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT -GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[{'x':pipeX,'y':y1},
        {'x':pipeX,'y':y2}  ]

    return pipe

if __name__=='__main__':
    ##this will be the main point where our game will start
    pygame.init()##initialize all pygame's module
    FPSCLOCK=pygame.time.Clock()##input a no from which the frame per second cant exit
    pygame.display.set_caption('Flappy Bird By Muskan')
    GAME_SPRITES['numbers']=(
        pygame.image.load('GALARY/sprites/0').convert_alpha(),#alpha makes easier to use the pictures in everyway or for quick bliting
        pygame.image.load('GALARY/sprites/1').convert_alpha(),
        pygame.image.load('GALARY/sprites/2').convert_alpha(),
        pygame.image.load('GALARY/sprites/3').convert_alpha(),
        pygame.image.load('GALARY/sprites/4').convert_alpha(),
        pygame.image.load('GALARY/sprites/5').convert_alpha(),
        pygame.image.load('GALARY/sprites/6').convert_alpha(),
        pygame.image.load('GALARY/sprites/7').convert_alpha(),
        pygame.image.load('GALARY/sprites/8').convert_alpha(),
        pygame.image.load('GALARY/sprites/9').convert_alpha(),
    )

    GAME_SPRITES['message']=pygame.image.load('GALARY/sprites/message').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('GALARY/sprites/base').convert_alpha()
    GAME_SPRITES['pipe']=(
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),#rotation in 180 degree
    pygame.image.load(PIPE).convert_alpha()
    )

##audio player
    #GAME_SOUNDS['die']=pygame.mixer.Sound('GALARY/audio/die.wav.mp3')
    #GAME_SOUNDS['hit']=pygame.mixer.Sound('GALARY/audio/hit.wav.mp3')
    #GAME_SOUNDS['point']=pygame.mixer.Sound('GALARY/audio/point.wav.mp3')
    #GAME_SOUNDS['swoosh']=pygame.mixer.Sound('GALARY/audio/swoosh.wav.mp3')
    #GAME_SOUNDS['wing']=pygame.mixer.Sound('GALARY/audio/wing.wav.mp3')

    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()##shows the welcome screen to the user until she presses a button
        maingame()#this is the main game function