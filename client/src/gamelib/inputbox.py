# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string, math
import threading
from pygame.locals import *

class InputArea(threading.Thread):

    def __init__(self, screen, x, y, width, height, title = "", nature = "", content = ""):
        
        threading.Thread.__init__(self)
        
        self.title = title
        self.nature = nature
        self.content = content
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        
        self.lines = []
        
        self.color = (255, 255, 255)
                            
        pygame.display.flip()    

    
    def add_line(self, line):
        self.lines.append(line)
        print "added line " + line
        
    def add_char(self, char):
        self.content = self.content + char
        
    def del_char(self):
        self.content = self.content[0:len(self.content)-1]
    
    def get_rect(self):
        return self.x, self.y, self.width, self.height
    
    def contains(self, x, y):
        return x > self.x and x < self.x+self.width and y > self.y and y < self.y+self.width 
    
    def set_focus(self, focus=True):
        if focus:
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)
    
    def draw(self):
        self.fontobject = pygame.font.Font(None, (int)(math.floor(self.screen.get_width() / 20)))
        pygame.draw.rect(self.screen, (0,0,0),
                       (self.x + 2, self.y + 2, self.width-4, self.height-4), 0)
        pygame.draw.rect(self.screen, (255,255,255),
                       (self.x, self.y, self.width, self.height), 1)  
        
        if len(self.title) != 0:            
            self.screen.blit(self.fontobject.render(self.title, 1, (255,255,255)),
                    (self.x, self.y - 24))
        if len(self.nature) != 0:
            self.screen.blit(self.fontobject.render(self.nature, 1, self.color),
                    (self.x - len(self.nature) - (int)(self.width/2), self.y - 9))
        i = 0
        for line in self.lines:
            self.screen.blit(self.fontobject.render(line, 1, (255,255,255)),
                (self.x + 10, i * 30 + 10 + self.y))
            i += 1
            
        #Cursor
#         self.screen.blit(self.fontobject.render("|", 1, (255,255,255)),
#                 (self.x + len(self.content) * 14, self.y))
            
        self.screen.blit(self.fontobject.render(self.content, 1, (255,255,255)),
                   (self.x + 2, self.y + 2))
            

    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass
    
    def get_input(self):
        th = threading.Thread(target=self.ask())
        th.start()
        #print 'Thread: ' + th.name()
        
    
    def get_content(self):
        return str(self.content)
    
        
    def update(self, events):
#         "ask(screen, question) -> answer"
        for event in events:
            if event.type == KEYDOWN:
                inkey = event.key
                if inkey == K_BACKSPACE:
                    self.del_char()
                elif inkey == K_RETURN:                
                    break        
                elif inkey <= 127:
                    self.add_char(chr(inkey))
            #TODO Me dislikes this shit
           # return self.content
    
