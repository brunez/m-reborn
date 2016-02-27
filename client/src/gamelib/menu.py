#! /usr/bin/env python

import pygame, sys, game
from pygame.locals import *

from game import *
from ezmenu import *
from network_menus import *
from data import *
from cutscenes import *
from pickle import FALSE

#===============================================================================
# MENU CHOICE CONSTANTS
#===============================================================================

NEW_GAME = 0
CONTINUE = 1
HOST_GAME = 2
JOIN_GAME = 3
HELP = 4
QUIT = 5

def RunGame(screen):
    game.Game(screen)
    #play_music("title.ogg", 0.75)

def HostGame(screen):
    HostMenu(screen)
    #play_music("title.ogg", 0.75)
    
def JoinGame(screen):
    JoinMenu(screen)
    #play_music("title.ogg", 0.75)
    
def ContinueGame(screen):
    Game(screen, True)
    #play_music("title.ogg", 0.75)
               
def Help(screen):
    cutscene(screen, ["HELP",
    "",
    "Move: Arrow Keys",
    "Jump: Z key",
    "Return: Esc = return",
    "Note: Jump on enemies to kill them!",
    ""])
    
class Menu(object):    

    def __init__(self, screen, options):
        self.screen = screen
#        self.menu = EzMenu(["NEW GAME", lambda: RunGame(screen)], ["CONTINUE", lambda: ContinueGame(screen)], ["HOST GAME", lambda: HostGame(screen)], ["JOIN GAME", lambda: JoinGame(screen)], ["HELP", lambda: Help(screen)], ["QUIT GAME", sys.exit])

                #Old ezmenu
        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options)*self.font.get_height()
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()
        
        

        self.set_highlight_color((255, 0, 0))
        self.set_normal_color((255, 255, 255))
        self.center_at(300, 400)
        self.set_font(pygame.font.Font(filepath("fonts/font.ttf"), 16))
        self.bg = load_image("menu.png")
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(filepath("fonts/super-mario-64.ttf"), 45)
        #play_music("title.ogg", 0.75)
        self.clock = pygame.time.Clock()
        
        
        
        
        events = pygame.event.get()
        self.draw(self.screen)    
        
    def start(self):
        return self.main_loop()
  
    def main_loop(self):
        while 1:
            self.clock.tick(40)
            events = pygame.event.get()
            selection_made = False
            
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        self.option += 1
                    if e.key == pygame.K_UP:
                        self.option -= 1
                    if e.key == pygame.K_RETURN:
                        selection_made = True        
                    if e.type == QUIT:
                        pygame.quit()
                        return
                    if e.type == KEYDOWN and e.key == K_ESCAPE:
                        pygame.quit()
                        return
                
            if self.option > len(self.options)-1:
                self.option = 0
            if self.option < 0:
                self.option = len(self.options)-1
                
            self.screen.blit(self.bg, (0, 0))
            ren = self.font.render("DEMO by Morp 2009", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 70))

            ren = self.font2.render("Super Mario", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 235))

            
            
            self.draw(self.screen)
            pygame.display.flip()
            
            if selection_made:
                return self.option

    def draw(self, surface):
        i=0
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, ((self.x+self.width/2) - ren.get_width()/2, self.y + i*(self.font.get_height()+4)))
            i+=1

    def set_pos(self, x, y):     
        self.x = x
        self.y = y
        
    def set_font(self, font):
        self.font = font
        
    def set_highlight_color(self, color):
        self.hcolor = color
        
    def set_normal_color(self, color):
        self.color = color
        
    def center_at(self, x, y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)