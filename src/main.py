import pygame, math, random, sys, re
from pygame.locals import *
from settings import *
from classes import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        pygame.display.set_caption(TITLE)

        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        self.scenes = [Scene(exbg),Scene(exbg2),Scene(exbg3)]
        self.current_scene = self.scenes[0]
        
        # Reading the file
        path = '../resources/script/'
        files = [
            open("{}Script_1.txt".format(path), "r"),
            open("{}Script_2a.txt".format(path), "r"),
            open("{}Script_3.txt".format(path), "r")
        ]
        for file in files:
            script = file.readlines()
            self.scenes.append(Scene(BACKGROUNDS[int(script[0])-1]))
            for i in range(2,len(script),6):
                dial_text = script[i][:-2]

                r1 = Response(script[i+1][:script[i+1].index(' (')], int(script[i+1][script[i+1].index('(')+1:script[i+1].index(')')]),scene_change=(')s' in script[i+1]))
                r2 = Response(script[i+2][:script[i+2].index(' (')], int(script[i+2][script[i+2].index('(')+1:script[i+2].index(')')]),scene_change=(')s' in script[i+2]))
                r3 = Response(script[i+3][:script[i+3].index(' (')], int(script[i+3][script[i+3].index('(')+1:script[i+3].index(')')]),scene_change=(')s' in script[i+3]))

                self.scenes[files.index(file)].add_dialogue(Dialogue(dial_text,[r1,r2,r3],exchar))

        self.next_scene = None

        self.scenes[1].add_dialogue(Dialogue("SCENE 2",[Response("ree",3),Response("ree",4),Response("ree",1)],exchar))

        self.game_state = "splash"

        self.text_anim = True
        self.fader = pygame.Surface((WIDTH,HEIGHT));self.fader.fill(BLACK)
        self.fading = False
        self.fade_alpha = 0
                                
           
    def run(self):
        
        # Game Loop
        while 1:
            while self.game_state == "splash":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        self.game_state = "speaking"

                self.window.fill(BLACK)
                self.text("S P L A S H S C R E E N","Courier New",30,WHITE,0,0,align="fullcenter")
                pygame.display.update()

            while self.game_state == "speaking":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        if self.current_scene.current_dialogue.responses[0].text == "END":
                            self.fade_alpha = 0
                            self.fade_out()
                        else:
                            self.game_state = "replying"

                if self.game_state != "speaking":
                    break

                self.window.blit(self.current_scene.bg,(0,0))

                # Draw Character
                self.window.blit(self.current_scene.current_dialogue.image,(0,0))

                overlay = pygame.Surface((680,150));overlay.set_alpha(128);overlay.fill(BLACK)
                self.window.blit(overlay,(200,510))

                if not self.fading:
                    if self.text_anim:
                        self.current_scene.current_dialogue.play_text(self.window,self.current_scene.bg,overlay,210,520)
                        self.text_anim = False
                    else:
                        tt = self.current_scene.current_dialogue.t
                        text_font = pygame.font.SysFont("arial", 25)
                        message = text_font.render(tt, True, WHITE)

                        if message.get_width() > WIDTH-410:
                            #split the message into sections 
                            index = int(len(tt)*(WIDTH-410)/(message.get_width()))
                            t1 = tt[:find_space_backwards(tt,index)]
                            t2 = tt[find_space_backwards(tt,index):]
                            self.text(t1,"arial",25,WHITE,210,520)
                            self.text(t2.strip(),"arial",25,WHITE,210,550)
                        else:
                            self.text(tt,"arial",25,WHITE,210,520)

                if self.fading:
                    if self.current_scene.current_dialogue.responses[0].text == "END":
                        if self.fade_alpha + 5 < 255:
                            self.fade_alpha += 5
                        else:
                            self.fading = False
                            self.game_state = "endscreen"
                            break
                    else:
                        if self.fade_alpha - 15 > 0:
                            self.fade_alpha -= 15
                        else:
                            self.fading = False
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))

                pygame.display.update()
                self.clock.tick(FPS)

            while self.game_state == "replying":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.MOUSEBUTTONUP:
                        # Check for button clicks
                        if mx >= 200 and mx <= WIDTH-200:
                            if my > 510 and my < 660:
                                if my > 510 and my < 560 and self.current_scene.current_dialogue.responses[0].text != "EMPTY":
                                    if self.current_scene.current_dialogue.responses[0].scene_change:
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[0].target_id-1]
                                        self.fade_out()
                                    else:
                                        self.current_scene.input(1)
                                elif my > 560 and my < 610 and self.current_scene.current_dialogue.responses[1].text != "EMPTY":
                                    if self.current_scene.current_dialogue.responses[1].scene_change:
                                        self.fade_out()
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[1].target_id-1]
                                    else:
                                        self.current_scene.input(2)
                                elif my > 610 and my < 660 and self.current_scene.current_dialogue.responses[2].text != "EMPTY":
                                    if self.current_scene.current_dialogue.responses[2].scene_change:
                                        self.fade_out()
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[2].target_id-1]
                                    else:
                                        self.current_scene.input(3)
                                self.text_anim = True
                                if not self.fading:
                                    self.game_state = "speaking"

                if self.game_state != "replying":
                    break

                # Clear screen
                self.window.blit(self.current_scene.bg,(0,0))

                # Draw Character
                self.window.blit(self.current_scene.current_dialogue.image,(0,0))

                # Grab mouse position
                mx,my = pygame.mouse.get_pos()

                # Declaring the faded overlay and selector
                overlay = pygame.Surface((680,150));overlay.set_alpha(128);overlay.fill(BLACK)
                selector = pygame.Surface((680,50));selector.set_alpha(128);selector.fill(BLACK)

                # Overlay Render
                self.window.blit(overlay,(200,510))

                # Selector Render
                if mx >= 200 and mx <= WIDTH-200:
                    if my > 510 and my < 560 and self.current_scene.current_dialogue.responses[0].text != "EMPTY":
                        self.window.blit(selector,(200,510))
                    elif my > 560 and my < 610 and self.current_scene.current_dialogue.responses[1].text != "EMPTY":
                        self.window.blit(selector,(200,560))
                    elif my > 610 and my < 660 and self.current_scene.current_dialogue.responses[2].text != "EMPTY":
                        self.window.blit(selector,(200,610))

                # Actual Replies
                for i in range(3): 
                    t = self.current_scene.current_dialogue.responses[i].text
                    if not t == "EMPTY":
                        self.text(t, "arial", 25, WHITE, 210, 518+50*i)
                    if t == "[next scene]":
                        self.text(t, "arial", 25, WHITE, -99, 518+50*i,align="center")

                if self.fading:
                    if self.fade_alpha + 15 < 255:
                        self.fade_alpha += 15
                    else:
                        self.game_state = "speaking"
                        self.current_scene = self.next_scene
                        break
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))

                pygame.display.update()
                self.clock.tick(FPS)

            while self.game_state == "endscreen":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        self.game_state = "splash"
                print(2)
                self.window.fill(BLACK)
                
                self.text("C R E D I T S", "Arial", 30, WHITE, 0,0,align="fullcenter")

    def text(self,text, font, size, color, x, y, align="free"):
        font_style = str(font)
        font_size = size

        text_font = pygame.font.SysFont(font_style, font_size)

        message = text_font.render(text, True, color)
        if(align == "center"):
            self.window.blit(message, (WIDTH/2-message.get_width()//2, y))
        elif(align == "fullcenter"):
            self.window.blit(message, (WIDTH/2-message.get_width()//2, HEIGHT/2-message.get_height()//2))
        else:
            self.window.blit(message, (x, y))

    def fade_out(self):
        self.fading = True

    def close(self):
        pygame.quit()
        sys.exit()

if (__name__ == "__main__"):
    g = Game()
    #g.read()
    #g.load()
    g.run()