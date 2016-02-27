'''
Created on Oct 27, 2012

@author: Runo
'''

import socket
import pygame
import server
import client
import inputbox
import sys
import random
import string
import data

IP = 0
NAME = 1

class ClientMenu(object):    

    def __init__(self, screen):
        self.screen = screen
        
        self.bg = data.load_image("menu4.png")
        self.font = pygame.font.Font(data.filepath("fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(data.filepath("fonts/super-mario-64.ttf"), 45)
        
        self.clock = pygame.time.Clock()        
        
        self.ip_input = inputbox.InputArea(self.screen, self.screen.get_width()/2 - 125, self.screen.get_height()/2 - 125, 250, 25, nature="Host IP")        
        self.name_input = inputbox.InputArea(self.screen, self.screen.get_width()/2 - 125, self.screen.get_height()/2 - 75, 250, 25, nature="Name")
        self.focused_input = None        
        self.set_focused_input(self.ip_input)

        self.connected = False

        self.ready = False
        
        self.name = ""        
        self.mode = None                
        self.level_name = ""

        
    def start(self):
        return self.main_loop()
  
    def request_to_join(self):
    
        self.client.send("rtj:"+self.name_input.get_content())
        self.connected = True
        print "RTJing"

    def set_game_info(self, info):
        self.game_info = info
        
    def set_id(self, player_id):
        self.id = player_id

    def set_ready(self, ready):
        self.ready = ready
        print "Client ready"
        
    def set_connected(self, connected):    
        self.connected = connected
        
    def set_mode(self, mode):
        self.mode = mode
        
    def set_level_name(self, level_name):
        self.level_name = level_name
    
    def set_focused_input(self, focused_input):        
        if self.focused_input != None:
            self.focused_input.set_focus(False)
        self.focused_input = focused_input
        self.focused_input.set_focus(True)
    
    
    def main_loop(self):
        while True:
            if self.connected:
                self.client.receive()
            self.clock.tick(40)
            events = pygame.event.get()
            self.focused_input.update(events)
#             self.ip_input.update(events)
#             self.name_input.update(events)
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
                if e.type == pygame.KEYDOWN: 
                    if e.key == pygame.K_ESCAPE:
                        #self.client.close()
                        pygame.quit()
                        return
                    if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:                    
                        self.host = self.ip_input.get_content()
                        print "Host at client: ", self.host
                        self.client = client.Client(self.host, 9999, self)
                        self.request_to_join()
                    elif e.key == pygame.K_DOWN:
                        self.set_focused_input(self.name_input)
                    elif e.key == pygame.K_UP:
                        self.set_focused_input(self.ip_input)    
                
            self.screen.blit(self.bg, (0, 0))                        

            #display_text_field(self.screen, "Server IP", [], 300, 25)    
            self.ip_input.draw()
            self.name_input.draw()
#            host = self.ip_input.ask()
                
#            self.menu.draw(self.screen)
            pygame.display.flip()
            
            #TODO Niapalandia...
            if self.ready:
                return [self.game_info, self.client, self.id, self.mode, self.level_name]
    