import pygame, math, random, sys, re
from pygame.locals import *
from settings import *
from classes import *
pygame.init()

class Game:
    def __init__(self):
            # Reading the file
        file = open("Chapter_1_Script.txt", "r")
        count = 1
        message = file.readlines()
        option1 = []
        option2 = []
        option3 = []
        dialog = []
        transition = []
        option1path = []
        option2path = []
        option3path = []
        a = 0
        temp = 0
        while message[a] != "END\n":
              temp = message[a]
              dialog.append(temp[4:])
              a=a+1
        a = a+1
 
        for x in range (0,len(dialog)):
              a = a+1
              option1.append(message[a])
              a = a+1
              option2.append(message[a])
              a = a+1
              option3.append(message[a])
              a = a+1

        for x in option1:
              temp2 = re.findall(r'\d+',x)
              if(len(temp2) == 0):
                   option1path.append(-1)
              else:
                   option1path.append((temp2[0]))

        for x in option2:
              temp2 = re.findall(r'\d+',x)
              if(len(temp2) == 0):
                   option2path.append(-1)
              else:
                   option2path.append((temp2[0]))

        for x in option3:
              temp2 = re.findall(r'\d+',x)
              if(len(temp2) == 0):
                   option3path.append(-1)
              else:
                   option3path.append((temp2[0]))
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        pygame.display.set_caption(TITLE)

        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        self.scenes = [Scene(exbg),Scene(exbg2)]
        self.current_scene = self.scenes[0]
        a = 0
        for x in dialog:
                self.current_scene.add_dialogue(Dialogue(x[:-1],[Response(option1[a][:-4],(int)(option1path[a])),Response(option2[a][:-4],(int)(option2path[a])),Response(option3[a][:-4],(int)(option3path[a]))    ],exchar))
                a = a+1
                                                
       # self.current_scene.add_dialogue(Dialogue("Dialogue 0",[Response("z",1),Response("z",1),Response("z",1)],exchar))
       # self.current_scene.add_dialogue(Dialogue("RANDOM GIRL: Hi! I haven't seen you around ... nice to meet you!",[Response("Likewise! What's your name?",2),Response("Ew, get away from me",3),Response("Gtfo cuz u know u a thot",1,scene_change=True)],exchar))
       # self.current_scene.add_dialogue(Dialogue("Dialogue 2",[Response("3",3),Response("4",4),Response("1",1)],exchar))
       # self.current_scene.add_dialogue(Dialogue("Dialogue 3",[Response("4",4),Response("1",1),Response("2",2)],exchar))
       # self.current_scene.add_dialogue(Dialogue("Dialogue 4",[Response("1",1),Response("2",2),Response("3",3)],exchar))

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
                self.text("S P L A S H S C R E E N", "Courier New",30,WHITE,0,0,align="center")
                pygame.display.update()

            while self.game_state == "speaking":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
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
                                if my > 510 and my < 560:
                                    if self.current_scene.current_dialogue.responses[0].scene_change:
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[0].target_id]
                                        self.fade_out()
                                    else:
                                        self.current_scene.input(1)
                                elif my > 560 and my < 610:
                                    if self.current_scene.current_dialogue.responses[1].scene_change:
                                        self.fade_out()
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[1].target_id]
                                    else:
                                        self.current_scene.input(2)
                                elif my > 610 and my < 660:
                                    if self.current_scene.current_dialogue.responses[2].scene_change:
                                        self.fade_out()
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[2].target_id]
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
                    if my > 510 and my < 560:
                        self.window.blit(selector,(200,510))
                    elif my > 560 and my < 610:
                        self.window.blit(selector,(200,560))
                    elif my > 610 and my < 660:
                        self.window.blit(selector,(200,610))

                # Actual Replies
                for i in range(3): 
                    t = self.current_scene.current_dialogue.responses[i].text
                    
                    self.text(t, "arial", 25, WHITE, 210, 518+50*i)

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

    def text(self,text, font, size, color, x, y, align="free"):
       font_style = str(font)
       font_size = size

       text_font = pygame.font.SysFont(font_style, font_size)

       message = text_font.render(text, True, color)
       if(align == "center"):
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

