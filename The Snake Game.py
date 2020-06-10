#Import Modules...............................................................
from os import environ
import itertools
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'       #<-------------- Hide Wellcome Pygame Prompt
environ['SDL_VIDEO_CENTERED'] = '1'               #<------------- Open Pygame Window To Center Of Screen
import pygame
import pygame.freetype
import random
import math
from pygame.locals import *
from threading import Thread
from time import sleep
from tkinter import *
from tkinter import messagebox  
import os,sys
import webbrowser
import numpy as np
import pickle

# Global Variables And Colors
appleonscreen = 0
time_change  = 10
flag = True
count_for_thread = 0
score = 0
playername = ""
high_scor = 0
Music_mute = False
Full_Mute = False
Sound_Mute = False

WINSIZE = [800, 606]  #<------------ Main Window X,Y
WHITE = [0,0,0]
BLACK = [255,255,255]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,0]
GREY = [105,105,105]
BLOCKSIZE = [20,20]
sky_blue = [0,255,255]
bisque1 = [255,228,196]
cadetblue1 = (152,245,255)
cadetblue= (95,158,160)
bisque4	= (139,125,107)
aquamarine2 = (118,238,198)
aqua= (0,255,255)
light_slate_blue = (132,112,255)
black = (0,0,0)
white = (255,255,255)
cyan = (0,255,255)
yellow = (255,255,0)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)
pink = (255,182,194)
violet = (59,0,93)
bright_red = (255,0,0)
bright_green = (0,255,0)
game = False
snake = "/snakegreenc.png"          #<--------#Default Snake Body (Green)
snake_h = "/snakegreen.png"         #<--------#Default Snake Head (Green)
s_over =  True
##############################

def resource_path():   #<-------- Generate Where The Py File Run Path and add Resource
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(CurrentPath, 'Resources')
    newPath = path.replace(os.sep, '/')
    return newPath

file = resource_path()       #<-------- Get Where The Py File Run Path


# Open High.txt For Get HighScore If Missing It Create A New High.txt And Set High Score = 0
try:
    with open (file+'/High.txt', 'rb') as fp1:        
        list_ = pickle.load(fp1)
        #print(list_)
        fp1.close()
        
    high_scor = list_[0][1]
except:
    list_ = []
    high_scor = 0


col2 =[]     #<----------- Add Colors For Snake Color In Menu
for i in range (20):
    col = tuple(np.random.randint(256, size=3))
    col2.append(col)

#Global Timer for generate new apple in 10 seconds
def timer():
    global appleonscreen,time_change
    while flag == True:
        while time_change >0:
            time_change -= 1
            sleep(1)   #waits 45 seconds
        appleonscreen = 0

t1 = Thread(target=timer) #<- For Run Timer Function in Background

#Initialized Sounds and Sounds Files and Set Background Music Volume
pygame.mixer.init()
bm1= file+"/bm1.wav"       
bm2= file+"/bm2.wav"

pygame.mixer.music.set_volume(0.04)         #<-------BackGround Music Volume

eat_sound = pygame.mixer.Sound(file+"/eat.wav")
die_sound = pygame.mixer.Sound(file+"/die.wav")


#Main Game Screen
def main():
    global appleonscreen,time_change,score,flag,count_for_thread,Music_mute,Full_mute,Sound_Mute,game,high_scor
    game = False
    if Music_mute == False and Full_Mute == False:
        pygame.mixer.music.play(-1)
    
    #For Show Good Bye Screen On Close
    def close():
        global time_change,flag,high_scor
        flag = False
        time_change = 0
        screen.fill(WHITE)
        font = pygame.font.Font((file+"/f5.ttf"), 100)
        pygame.mixer.music.stop()
        text_surface = font.render("GOOD BYE !!", True, BLACK)
        screen.blit(text_surface, (235,260))
        pygame.display.flip()
        if score > high_scor:   #<--- If It's a new high score save the score and name to High.txt
            high_scor = score
            newdata = (playername, score)
            list_.insert(0, newdata)
            if (len(list_)) == 5:
                list_.pop(4)
            with open(file+'/High.txt', 'wb') as fp:
                pickle.dump(list_, fp)
                fp.close()
        sleep(2)        #<---- Wait 2 Seconds to show good bye
        exit()

    showstartscreen = 1         #<---- It's Optional 

    while 1:
        if score > high_scor:       #<--- If It's a new high score save the score and name to High.txt(For Press N)
            high_scor = score
            newdata = (playername, score)
            list_.insert(0, newdata)
            if (len(list_)) == 5:
                list_.pop(4)
            with open(file+'/High.txt', 'wb') as fp:
                pickle.dump(list_, fp)
                fp.close()
        ######## CONSTANTS
        UP = 1
        DOWN = 3
        RIGHT = 2
        LEFT = 4
        MAXX = 760
        MINX = 20
        MAXY = 560
        MINY = 80
        SNAKESTEP = 20
        TRUE = 1
        FALSE = 0
        ######## VARIABLES

        direction = RIGHT # 1=up,2=right,3=down,4=left
        snakexy = [300,400]
        snakelist = [[300,400],[280,400],[260,400]]
        counter = 0
        score = 0
        time_change = 10
        newdirection = RIGHT
        snakedead = FALSE
        gameregulator = 6
        gamepaused = 0
        growsnake = 0  # added to grow tail by two each time
        snakegrowunit = 2 # added to grow tail by two each time

        # Game Running Screen
        
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption("The Snake Game")
        screen.fill(cadetblue)


        def M_mute():   # If Press Music Mute Key
            global Music_mute
            Music_mute = True
            pygame.mixer.music.pause()
        def UNM_mute():         # If Press Music Un-Mute Key
            global Music_mute,Full_mute
            Music_mute = False
            Full_mute = False
            pygame.mixer.music.unpause()
        
        def f_mute_t2():    # If Press Full Mute Key
            global Full_Mute,Music_mute,Sound_Mute
            pygame.mixer.music.pause()
            Music_mute = True
            Sound_Mute = True
            Full_Mute = True
        def f_mute_f2():        # If Press Full Un-Mute Key
            global Full_Mute,Music_mute,Sound_Mute
            pygame.mixer.music.unpause()
            Music_mute = False
            Sound_Mute = False
            Full_Mute = False

        def s_mute_t2():        # If Press Sound Mute Key
            global Sound_Mute
            Sound_Mute = True

        def s_mute_f2():        # If Press Sound Un-Mute Key
            global Sound_Mute
            Sound_Mute = False
            Full_Mute = False
        
        # Change Background Music To  Game BackGround Music And Check If It Mute or Un-Mute
        
        pygame.mixer.music.load(bm1)
        pygame.mixer.music.play(-1) 
        if Music_mute == False and Full_Mute == False:
            pygame.mixer.music.unpause()
        if Music_mute == True and Full_Mute == True:
            pygame.mixer.music.pause()    
        

        #print("start")

        #if showstartscreen == TRUE:
        xrange=range
        showstartscreen = FALSE
        screen.fill(BLUE)
        font = pygame.font.Font((file+"/f2.ttf"), 160)
        for i in reversed(xrange(4)):
            screen.fill(BLUE)
            if i > 0:
                text_surface = font.render(str(i), True, BLACK)
                screen.blit(text_surface, (340,190))
            elif i == 0:
                text_surface = font.render("Go!!!", True, BLACK)
                screen.blit(text_surface, (220,190))
            pygame.display.flip()
            clock.tick(8) 
            sleep(1)
            time_change = 10
        
        if count_for_thread == 0:    #For Prevent Thread To Call More than 1 time
            time_change = 10
            t1.start()
            count_for_thread = 1
        
        while not snakedead:
            ###### get input events  ####

            for event in pygame.event.get():
                if event.type == QUIT:
                    close()
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_LEFT] or pressed_keys[K_a] : newdirection = LEFT
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]: newdirection = RIGHT
            if pressed_keys[K_UP] or pressed_keys[K_w]: newdirection = UP
            if pressed_keys[K_DOWN] or pressed_keys[K_s]: newdirection = DOWN
            if pressed_keys[K_m]: f_mute_t2()
            if pressed_keys[K_n]: f_mute_f2()
            
            if pressed_keys[K_b]: M_mute()
            if pressed_keys[K_v]: UNM_mute()
            
            if pressed_keys[K_c]: s_mute_t2()
            if pressed_keys[K_x]: s_mute_f2()
            
            if pressed_keys[K_q]: snakedead = TRUE
            if pressed_keys[K_p]: gamepaused = 1
            ### wait here if p key is pressed until p key is pressed again
            
            while gamepaused == 1:
                paused = True
                for event in pygame.event.get():
                    if event.type == QUIT:
                        close()
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_r]:
                    gamepaused = 0
                    paused = False
                clock.tick(10)


            ### added gameregulator because setting a very low clock ticks
            ### caused the keyboard input to be hit and miss.  So I up the
            ### gameticks and the input and screen refresh is at this rate
            ### but the snake moving and all other logic is at the slower
            ### "regulated" speed

            if gameregulator == 6:
                
                ####### lets make sure we can't go back the reverse direction
                if newdirection == LEFT and not direction == RIGHT:
                    direction = newdirection
                
                elif newdirection == RIGHT and not direction == LEFT:
                    direction = newdirection

                elif newdirection == UP and not direction == DOWN:
                    direction = newdirection

                elif newdirection == DOWN and not direction == UP:
                    direction = newdirection

                ##### now lets move the snake according to the direction
                ##### if we hit the wall the snake dies
                ##### need to make it less twitchy when you hit the walls


                if direction == RIGHT:
                    snakexy[0] = snakexy[0] + SNAKESTEP
                    if snakexy[0] > MAXX:
                        snakedead = TRUE

                elif direction == LEFT:
                    snakexy[0] = snakexy[0] - SNAKESTEP
                    if snakexy[0] < MINX:
                        snakedead = TRUE

                elif direction == UP:
                    snakexy[1] = snakexy[1] - SNAKESTEP
                    if snakexy[1] < MINY:
                        snakedead = TRUE

                elif direction == DOWN:
                    snakexy[1] = snakexy[1] + SNAKESTEP
                    if snakexy[1] > MAXY:
                        snakedead = TRUE

                ### is the snake crossing over itself
                ### had to put the > 1 test in there as I was
                ### initially matching on first pass otherwise - not sure why

                if len(snakelist) > 3 and snakelist.count(snakexy) > 0:
                    snakedead = TRUE



                #### generate an apple at a random position if one is not on screen
                #### make sure apple never appears in snake position
                
                if appleonscreen == 0:
                    time_change = 10
                    good = FALSE
                    while good == FALSE:
                        x = random.randrange(1,39)
                        y = random.randrange(5,29)
                        applexy = [int(x*SNAKESTEP),int(y*SNAKESTEP)]
                        if snakelist.count(applexy) == 0:
                            good = TRUE
                    appleonscreen = 1
                    

                #### add new position of snake head
                #### if we have eaten the apple don't pop the tail ( grow the snake )
                #### if we have not eaten an apple then pop the tail ( snake same size )

                snakelist.insert(0,list(snakexy))
                if snakexy[0] == applexy[0] and snakexy[1] == applexy[1]:
                    appleonscreen = 0
                    score = score + 1
                    growsnake = growsnake + 1
                    time_change = 10
                    
                    #myfont = pygame.font.SysFont('Comic Sans MS',30)
                    #text_surface = myfont.render('Hi',False,(0,0,0))
                    
                    
                    if Sound_Mute == False and Full_Mute == False:
                        eat_sound.play()
                elif growsnake > 0:
                    growsnake = growsnake + 1
                    if growsnake == snakegrowunit:
                        growsnake = 0
                else:
                    snakelist.pop()



                gameregulator = 0


            ###### RENDER THE SCREEN ###############

            ###### Clear the screen
            screen.fill(BLUE)
            
            ###### Draw the screen borders
            ### horizontals
            pygame.draw.line(screen,aqua,(4,4),(794,4),2)
            pygame.draw.line(screen,aqua,(4,69),(794,69),2)
            pygame.draw.line(screen,aqua,(4,600),(794,600),2)
            
            ### verticals
            pygame.draw.line(screen,aqua,(4,4),(4,600),2)
            pygame.draw.line(screen,aqua,(794,4),(794,600),2)

            ###### Print the score
            
            font = pygame.font.Font((file+"/f1.ttf"), 35)
            
            text_surface = font.render(str(playername)+" Score: " + str(score), True, light_slate_blue)
            screen.blit(text_surface, (10,2))
            
            text_surface = font.render("New Appel In: "+str(time_change), True, light_slate_blue)
            screen.blit(text_surface, (250,32))
            
            if score > high_scor or score == high_scor: #Change High Score with Score
                text_surface = font.render("High Score: " + str(score), True, light_slate_blue)
                screen.blit(text_surface, (528,2))
            elif score < high_scor:  
                text_surface = font.render("High Score: " + str(high_scor), True, light_slate_blue)
                screen.blit(text_surface, (528,2))
                

            
            ###### Output the array elements to the screen as rectangles ( the snake)
            for element in snakelist:
                #pygame.draw.rect(screen,RED,Rect(element,BLOCKSIZE))
                image2 = pygame.image.load(str(file+snake))
                s_head =  pygame.image.load(str(file+snake_h))
                
                
                screen.blit(s_head,(snakelist[0][0],snakelist[0][1]))
                
                screen.blit(image2,(element)) 
            
            ###### Draw the apple snakeyellow.png snakegreen
            #pygame.draw.rect(screen,GREEN,Rect(applexy,BLOCKSIZE))
            image = pygame.image.load(str(file+"/food.png"))
            screen.blit(image,(applexy)) 
            #pygame.draw.rect(screen,GREEN,Rect(apple,BLOCKSIZE))
            
            
            ###### Flip the screen to display everything we just changed
            pygame.display.flip()



            gameregulator = gameregulator + 1

            clock.tick(25)

        if snakedead == TRUE:  #Game Over Menu 
            pygame.mixer.music.pause()
            if Sound_Mute == False and Full_Mute == False:
                die_sound.play()
            screen.fill(WHITE)
            if Music_mute == False and Full_Mute == False:
                pygame.mixer.music.load(bm2)
                pygame.mixer.music.play(-1)
            font = pygame.font.Font((file+"/f2.ttf"), 48)
            text_surface = font.render("GAME OVER !!", True, BLACK)
            screen.blit(text_surface, (270,160))
            text_surface = font.render("Your Score Is: " + str (score), True, BLACK)
            screen.blit(text_surface, (240,250))
            
            font = pygame.font.Font((file+"/f3.ttf"), 24)
            text_surface = font.render("Press Q to quit", True, BLACK)
            screen.blit(text_surface, (320,400))
            text_surface = font.render("Press N to play again", True, BLACK)
            screen.blit(text_surface, (290,450))
            
            text_surface = font.render("Press M to go back Main Menu", True, BLACK)
            screen.blit(text_surface, (242,500))
            
            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        close()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]: close()
                if pressed_keys[K_m]: menu()
                if pressed_keys[K_n]: break

                clock.tick(10)

def menu():     #<-------Game Menu
    
    global s_over,game,time_change,flag,Music_mute,Full_Mute,Sound_Mute,snake,high_scor,snake_h
    pygame.init()
    pygame.mixer.music.load(bm2)        #<-------Change Background Music To 
    pygame.mixer.music.play(-1)
    #Play Background Music When Bg Music Mute or Full Mute is Disable
    if Music_mute == False and Full_Mute == False:
        pygame.mixer.music.unpause()
    elif Music_mute == True and Full_Mute == True:
        pygame.mixer.music.pause()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('The Snake Game')    #Game Window Title Bar Name
    clock = pygame.time.Clock()

    gameIcon = pygame.image.load(file+'/icon.png')  #Game Window Title Bar Icon
    
    #Main Menu Back Ground
    intbg = pygame.image.load(file+"/Backg.jpg")
    intbg = pygame.transform.scale(intbg, (800,606))
    pygame.display.flip()

    #Setting Menu Back Ground
    stnbg = pygame.image.load(file+'/settbg.png')
    stnbg = pygame.transform.scale(stnbg, (800,606))
    pygame.display.flip()

    pygame.display.set_icon(gameIcon)       #Game Window Title Bar Icon Set

    recta = intbg.get_rect()

    recta = recta.move((0,0))

    setta = stnbg.get_rect()

    setta = recta.move((0,0))

    #Instraction Menu Back Ground
    istcbg = pygame.image.load(file+'/nxtimg.jpg')
    istcbg = pygame.transform.scale(istcbg, (800,606))
    pygame.display.flip()


    #HighScore Menu Back Ground
    highbg = pygame.image.load(file+'/highbg.jpg')
    highbg = pygame.transform.scale(highbg, (800,606))
    pygame.display.flip()

    rectis = istcbg.get_rect()

    rectis = rectis.move((0,0))
    screen.blit(istcbg, rectis)

    rectis = highbg.get_rect()

    rectis = rectis.move((0,0))
    screen.blit(highbg, rectis)
    
    if score > high_scor: #If High Score Smaller Than Score Save High Score
        high_scor = score
        newdata = (playername, score)
        list_.insert(0, newdata)
        if (len(list_)) == 5:   #If High Score List get more than 4 value delete last value
            list_.pop(4)
        with open(file+'/High.txt', 'wb') as fp:
            pickle.dump(list_, fp)
            fp.close()
    
    def close2():   #Show Good Bye Screen
        global time_change,flag,high_scor
        flag = False
        time_change = 0
        screen.fill(WHITE)
        font = pygame.font.Font((file+"/f5.ttf"), 100)
        pygame.mixer.music.stop()
        text_surface = font.render("GOOD BYE !!", True, BLACK)
        screen.blit(text_surface, (235,260))
        pygame.display.flip()
        if score > high_scor:       #If High Score Smaller Than Score Save High Score
            high_scor = score
            newdata = (playername, score)
            list_.insert(0, newdata)
            if (len(list_)) == 5:       #If High Score List get more than 4 value delete last value
                list_.pop(4)
            with open(file+'/High.txt', 'wb') as fp:
                pickle.dump(list_, fp)
                fp.close()
        sleep(2)
        exit()

    if game == False:
        def round_rect(surface, rect, color, rad=28, border=0, inside=(0,0,0,0)):
            """
            Draw a rect with rounded corners to surface.  Argument rad can be specified
            to adjust curvature of edges (given in pixels).  An optional border
            width can also be supplied; if not provided the rect will be filled.
            Both the color and optional interior color (the inside argument) support
            alpha.
            """
            rect = pygame.Rect(rect)
            zeroed_rect = rect.copy()
            zeroed_rect.topleft = 0,0
            image = pygame.Surface(rect.size).convert_alpha()
            image.fill((0,0,0,0))
            _render_region(image, zeroed_rect, color, rad)
            if border:
                zeroed_rect.inflate_ip(-2*border, -2*border)
                _render_region(image, zeroed_rect, inside, rad)
            surface.blit(image, rect)


        def _render_region(image, rect, color, rad):
            """Helper function for round_rect."""
            corners = rect.inflate(-2*rad, -2*rad)
            for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
                pygame.draw.circle(image, color, getattr(corners,attribute), rad)
            image.fill(color, rect.inflate(-2*rad,0))
            image.fill(color, rect.inflate(0,-2*rad))



        def button(msg,x,y,w,h,ic,ac,r,action): #Get Mouse Movment
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            #print(mouse)
            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                round_rect(screen, (x-r,y-r,w+(2*r),h+(2*r)), ac)
                if click[0] == 1 and action != None:
                    action()         
            else:
                round_rect(screen, (x-2,y-2,w+4,h+4), ic)
            smallText = pygame.font.SysFont("calibri",30)
            textSurf, textRect = text_objects(msg, smallText)
            textRect.center = ( (round(x+(w/2))), (round(y+(h/2))) )
            screen.blit(textSurf, textRect)
            


        def urlfb():        #Open Fb page with default web browser
            new = 2
            url = "https://www.facebook.com/Isjtijlfti.patra"
            webbrowser.open(url,new=new)

        def urlin():        #Open Github page with default web browser
            new = 2
            url = "https://github.com/Hrishikesh7665"
            webbrowser.open(url,new=new)

        def urltw():        #Open HackerRank page with default web browser
            new = 2
            url = "https://www.hackerrank.com/Hrishikesh7665"
            webbrowser.open(url,new=new)


        def misc(): #Un mute Bg Music and Full Mute
            global Music_mute,Full_mute
            Music_mute = False
            Full_mute = False
            pygame.mixer.music.unpause()
        
        def musc(): #Mute Bg Music
            global Music_mute
            Music_mute = True
            pygame.mixer.music.pause()

        def f_mute_t(): #Full Mute
            global Full_Mute,Music_mute,Sound_Mute
            pygame.mixer.music.pause()
            Music_mute = True
            Sound_Mute = True
            Full_Mute = True
        def f_mute_f(): #Full Un-Mute
            global Full_Mute,Music_mute,Sound_Mute
            pygame.mixer.music.unpause()
            Music_mute = False
            Sound_Mute = False
            Full_Mute = False
        
        def s_mute_t():     #Mute Game Sound
            global Sound_Mute
            Sound_Mute = True
        
        def s_mute_f():     #Un mute Game Sound and Full Mute
            global Sound_Mute,Full_Mute
            Sound_Mute = False
            Full_Mute = False
        
        def blkcolyl():         #Change Snake Color To Yellow
            global snake,snake_h
            snake = "/snakeyellowc.png"
            snake_h = "/snakeyellow.png"
            pygame.display.update()
            clock.tick(15)

        def blkcolgr():         #Change Snake Color To Green
            global snake,snake_h
            snake = "/snakegreenc.png"
            snake_h = "/snakegreen.png"
            pygame.display.update()
            clock.tick(15)
        
        def blkcolvo():         #Change Snake Color To Violet
            global snake,snake_h
            snake = "/snakevioletc.png"
            snake_h = "/snakeviolet.png"
            pygame.display.update()
            clock.tick(15)


        def text_objects(text, font):       #Function For Show Text
            textSurface = font.render(text, True, black)
            return textSurface, textSurface.get_rect()


                
        def game_intro():       #Show Game Intro Snake Load and other main menu buttons
            global s_over
            intro = True
            screen.blit(intbg, recta)
            s = [[180,120],[180,100],[160,100],[140,100],[120,100],[100,100],[100,120],[100,140],[100,160],[120,160],[140,160],[160,160],[180,160],[180,180],[180,200],[180,220],[160,220],[140,220],[120,220],[100,220],[100,200]]
            apple = [100,200]

            pygame.draw.rect(screen,(215,48,48),Rect(apple,BLOCKSIZE))
            
            clock.tick(8)
            if s_over == True:          #Snake Load
                pygame.display.flip()
                col = [(255,255,255),(0,5,255),(0,0,0)]
                for e in s:
                    pygame.draw.rect(screen,(random.choice(col2)),Rect(e,BLOCKSIZE))
                    pygame.display.flip()
                    clock.tick(5)
                    if e == ([100, 200]) :
                        for e in s:
                            pygame.draw.rect(screen,black,Rect(e,BLOCKSIZE))
                            pygame.display.flip()
                pygame.draw.rect(screen,black,Rect(e,BLOCKSIZE))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close2()
                #screen.blit(intbg, recta)
                largeText = pygame.font.SysFont("broadway",75)
                smallText = pygame.font.SysFont("forte",68)
                name = pygame.font.SysFont("Segoe UI", 25)
                TextSurf, TextRect = text_objects("The", smallText)
                #0, 255, 255
                TextRect.center = (320,162)
                
                screen.blit(TextSurf, TextRect)

                font = pygame.font.SysFont("arial", 64)
                text_surface = font.render("Nake Game", True, black)
                screen.blit(text_surface, (220,180))
                s_over =  True
                button("f",608,14,35,35,(59,89,239),(68,143,255),7,urlfb)
                button("g",662,14,35,35,(245, 255, 250),(248, 248, 255),7,urlin)
                button("H",719,14,35,35,(0,238,0),(0,128,0),7,urltw)

                button("Play",608,100,149,50,(106, 90, 205),(72, 61, 139),9,play_game)
                button("Instructions",608,177,149,50,(0, 206, 209),(64, 224, 208),9,instrc)
                button("Settings",608,257,149,50,(112,128,144),(192,192,192),9,sett)
                button("About",608,338,149,50,yellow,(255,255,100),9,info)
                button("High Scores",608,425,149,50,(127, 255, 180),(178, 255, 210),9,high)
                button("Exit",608,502,149,50,(205, 92, 92),(RED),9,close2)
                #pygame.display.flip()
                pygame.display.update()
                clock.tick(15)

        def sett():     #Setting Menu
            global s_over
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close2()
            
                screen.blit(stnbg, setta)
                
                bgdcol = pygame.font.SysFont("Segoe UI",40)
                blkcol = pygame.font.SysFont("Segoe UI",40)
                gmms = pygame.font.SysFont("Segoe UI",40)
                sppd = pygame.font.SysFont("Segoe UI",40)
                TextSurf3, TextRect3 = text_objects("Choose Snake Colour", bgdcol)
                TextSurf4, TextRect4 = text_objects("Game BG Music", blkcol)
                TextSurf5, TextRect5 = text_objects("Game Sound", sppd)
                TextSurf6, TextRect6 = text_objects("Full Mute",gmms)
                TextRect3.center = (227,90)
                TextRect4.center = (182,210)
                TextRect5.center = (156,330)
                TextRect6.center = (123,440)
                screen.blit(TextSurf3, TextRect3)
                screen.blit(TextSurf4, TextRect4)
                screen.blit(TextSurf5, TextRect5)
                screen.blit(TextSurf6, TextRect6)
                screen.blit(TextSurf4, TextRect4)
                s_over = True
                button("<- RETURN",302,540,150,50,(153,217,234),(163,227,244),9,game_intro)
                
                button("Green",100,125,100,50,green,bright_green,6,blkcolgr)
                button("Yellow",275,125,100,50,yellow,(255,255,100),6,blkcolyl)
                button("Purple",450,125,100,50,(138,43,226),(255,0,255),6,blkcolvo)
                
                button("Yes",100,245,100,50,green,bright_green,6,misc)
                button("No",275,245,100,50,red,bright_red,6,musc)

                button("Yes",100,365,100,50,green,bright_green,6,s_mute_f)
                button("No",275,365,100,50,red,bright_red,6,s_mute_t)

                button("On",100,475,100,50,green,bright_green,6,f_mute_t)
                button("Off",275,475,100,50,red,bright_red,6,f_mute_f)
                
                pygame.display.update()
                clock.tick(15)


        def info():     #About Menu
            global s_over
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close2()
            
                screen.fill(cyan)

                cred = pygame.font.SysFont("Algerian",60)
                cred1 = pygame.font.SysFont("Segoe UI",25)
                cred2 = pygame.font.SysFont("Segoe UI",25)

                TextSurf6, TextRect6 = text_objects("Credits :-",cred)
                TextSurf7, TextRect7 = text_objects("Contact Links-",cred1)
                TextSurf8, TextRect8 = text_objects("Developed By : Hrishikesh Patra",cred2)

                TextRect6.center = (392,100)
                TextRect7.center = (390,300)
                TextRect8.center = (390,200)

                screen.blit(TextSurf6, TextRect6)
                screen.blit(TextSurf7, TextRect7)
                screen.blit(TextSurf8, TextRect8)
                s_over = True
                button("<- RETURN",303,500,150,50,cyan,(100,255,255),6,game_intro)
                
                button("f",315,330,35,35,(59,89,239),(68,143,255),7,urlfb)
                button("g",373,330,35,35,(245, 255, 250),(248, 248, 255),7,urlin)
                button("H",431,330,35,35,(0,238,0),(0,128,0),7,urltw)

                pygame.display.update()
                clock.tick(15)
                
            

        def instrc():     #Introduction Menu
            global s_over
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close2()
                        
                screen.blit(istcbg, rectis)
                s_over = True
                button("<- RETURN",320,550,135,44,(153,217,234),(163,227,244),9,game_intro)
                pygame.display.update()
                clock.tick(15)


        def high():     #HighScore Menu
            global s_over
            font = pygame.freetype.SysFont("forte", 28, True, False)
            screen.blit(highbg, recta)
            pygame.display.flip()
            background = screen.copy()
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close2()

                screen.blit(background, (0, 0))
                
                
                #HighScore Name And Score Position
                x = 344         
                y = 244
                try:
                    with open (file+'/High.txt', 'rb') as fp1:      #Load High Score From High.txt
                        list_ = pickle.load(fp1)
                        fp1.close()
                        
                    high_scor = list_[0][1]
                except:
                    list_ = []
                for row in list_:
                    for cell in row:
                        font.render_to(screen, (x, y), str(cell), pygame.Color('dodgerblue'))
                        x += 206
                    y += 30
                    x = 344
                
                button("<- RETURN",320,550,135,44,(153,217,234),(163,227,244),9,game_intro)
                pygame.display.flip()
                clock.tick(60)


    def play_game():  #Play Game Call Main Menu
        game = True
        pygame.mixer.music.load(bm1)
        pygame.mixer.music.play(-1)
        if Music_mute == False and Full_Mute == False:
            pygame.mixer.music.unpause()
        elif Music_mute == True and Full_Mute == True:
            pygame.mixer.music.pause()
        
        main()
    if game == False:
        game_intro()


#Tkinter Window For Ask Player Name
ask_name_window = Tk()
ask_name_window.attributes('-topmost', True)
ask_name_window.iconbitmap(file+"/icon.ico")



def center_window(w=300, h=200):    #Center Tk Window (Upper)
    # get screen width and height
    ws = ask_name_window.winfo_screenwidth()
    hs = ask_name_window.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/4) - (h/2)
    ask_name_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
center_window(235,130)

#ask_name_window.geometry("235x110")
ask_name_window.title("Player Name")
ask_name_window.resizable(width=False, height =False)
ask_name_window.configure(bg='old lace')



def checkdetails():     #Player Name Conformation
    global playername
    playername = Name_entry.get()
    if (playername!=""):
        c2.config(text="Login Successful",bg='spring green')  
        confrom = messagebox.askquestion("confirmation","From Hrishikesh \nDo Any Change ?",default='no')  
        if confrom == 'no':
            pygame.mixer.music.load(bm2)
            pygame.mixer.music.play(-1)
            ask_name_window.destroy()
            menu()
        else:  
            c2.config(text="Change What You Want",bg='FloralWhite')  
    else:
        c2.config(text="Please Enter Your Name",bg='salmon')

svar = StringVar()
labl = Label(ask_name_window, textvariable=svar, height=1,width=235 )
labl.config(fg = 'lightgoldenrodyellow',font = ("Rockwell",10),justify = 'right',width = 300,background='black')



def shif():     #Show Slide Text
    shif.msg = shif.msg[1:] + shif.msg[0]
    svar.set(shif.msg)
    ask_name_window.after(150, shif)

shif.msg = '                   This Game Was Made By Hrishikesh Patra.  Contact --> hrishikesh.pgh.patra@gmail.com'
shif()
labl.pack()

Name_label = Label(ask_name_window,text = "Enter User Name",font=("mv boli","11"),bg='old lace')
Name_label.pack()
Name_entry = Entry(ask_name_window,font=("lucida handwriting","10"),bd=3)
Name_entry.focus()
Name_entry.pack()
c2 = Label(ask_name_window,text="",font=("forte","14"),bg='old lace')
c2.pack(side = TOP,anchor=CENTER)

ok_button = Button(ask_name_window,text = "Ok",bg='alice blue',font=("Harrington","10"),command = checkdetails,bd=3)
ok_button.pack(side = BOTTOM,anchor=CENTER)

def _delete_window():
    ask = messagebox.askquestion("Confirmation","Do You Want To Exit ?",icon='warning')
    if ask == 'yes':
        try:
            ask_name_window.destroy()
            #exit()
        except:
            pass


ask_name_window.protocol("WM_DELETE_WINDOW", _delete_window)
ask_name_window.mainloop()
