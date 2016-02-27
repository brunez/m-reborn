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

from pygame.locals import *
from data import *




def get_localhost():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("www.google.com", 9))
        client = s.getsockname()[0]
    except socket.error:
        client = "Unknown IP"
    finally:
        del s
    print "Obtained IP: " + client
    return client
    

class HostMenu(object):    

    def __init__(self, screen):
        self.screen = screen
   
        self.bg = load_image("menu4.png")
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(filepath("fonts/super-mario-64.ttf"), 45)
        
        #play_music("title.ogg", 0.75)
        self.clock = pygame.time.Clock()
        
        self.player_box = inputbox.InputArea(self.screen, self.screen.get_width()/2 - 125, self.screen.get_height()/2 - 125, 250, 250, "Players")            

        localhost = "127.0.0.1"
#        localhost = "192.168.0.195"
#        self.game = netgame.Game(screen, self.client, 0)
        
        self.server = server.Server(localhost, 9999, self.player_box, self)
#        self.client = client.Client(localhost, 9999, self, True)          
          
        
    def start(self):
#        self.client.send("rtj:host")        
        return self.main_loop()
         
  
    def set_game_info(self, info):
        self.game_info = info
  
    def main_loop(self):        
        while 1:
            self.server.receive()      
            self.clock.tick(40)
            events = pygame.event.get()
#            self.menu.update(events)
            for e in events:
                if e.type == QUIT:
                    self.server.close()
                    pygame.quit()                    
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    return      
                elif e.type == KEYDOWN and (e.key == K_RETURN or e.key == K_KP_ENTER):
                    self.server.sendall("start")
                    #TODO Return should be at the end
                    return [self.game_info, None, self.server, 0]
                    
#                    start(self.screen, self.client, 0, self.server)
#                    self.start(self.screen)              
                
            self.screen.blit(self.bg, (0, 0))
         #   self.screen.blit(ren, (320-ren.get_width()/2, 70))

            self.player_box.draw()
                
#            self.menu.draw(self.screen)
            pygame.display.flip()
