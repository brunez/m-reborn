#! /usr/bin/env python


import sys
import sprites
import camera
import game
import pygame
import data
import network
import math
import threading

from level import *

### Constants
INTRO_DELAY = 1
CLOCK_TICK = 60
#This indicates every how many frames the game state is synced
SYNC_FREQ = 30
SCREEN_WIDTH = 640

#ACTIONS
JUMP = str(0)
LEFT = str(1)
RIGHT = str(2)
STOP = str(3)
KEEP_JUMPING = str(4)
STOP_JUMPING = str(5)
#CAMERA MODES
COME_TOGETHER = 0
ON_YOUR_OWN = 1


#===============================================================================
#SERVER GAME CLASS 
#===============================================================================
class ServerGame(game.Game):

    #===============================================================================
    # Constructor
    # screen: The drawing surface 
    # server: The network server
    # game_info: The players that have joined the game
    # id: The id of the local player. 0 is the server in a LAN game.
    # 
    #===============================================================================
    def __init__(self, server, game_info, game_id, level_name):
        game.Game.__init__(self, game_info, game_id, level_name)
        self.server = server
        self.i = 0
        
        self.state_observers = []
        #The semaphores are used in case anyone has to wait for the loop to
        #end before doing something
        self.semaphores = []
        
        #Link this object to the sprites, so that they can notify it of events
        for s in self.obt_sprites:
            s.set_game(self)            
        for p in self.players:
            s.set_game(self)
     
        for b in sprites.baddie_collider_list:
            b.set_remote_role(network.ROLE_CLIENT)   
        for pc in sprites.player_collision_group:
            #TODO Niapa?            
            pc.set_default_remote_role() 
            
        self.pre_period = 500
        self.current_iteration = 0
     
    def add_state_observer(self, observer):
        self.state_observers.append(observer)
        
    def add_semaphore(self, sem):
        self.semaphores.append(sem)

    #This method sends the game state over the network for synchronization
    def send_game_state(self):
#         print "=========================Syncing========================="
        game_state = ["sync"]
        for e in self.game_state_elements:
            if self.is_visible(e):
#                print "Game state element at ", e.get_position()
                game_state.append(network.SpriteState(e.get_life(), e.get_position(), e.get_speed(), e.get_direction(), e.get_object_id()))
#         print "Sending sync state: ", game_state        
        self.server.sendall(game_state)
#         print "-------------------------Finished------------------------"
 
    #This method send the player state over the network for synchronization
    def send_player_state(self):
#        print "=========================Syncing========================="
        player_state = ["ply_sync"]
        for p in self.players:        
            player_state.append(network.PlayerState(p.get_life(), p.get_position(), p.get_speed(), p.get_direction(), p.has_won(), p.get_object_id()))
#        print "Sending player sync state: ", player_state        
        self.server.sendall(player_state)
#        print "-------------------------Finished------------------------"
    

    #This method determines if a sprite is visible by any player and should be synchronized
    def is_visible(self, sprite):
        visible = False
        for p in self.players:
            if math.fabs(sprite.rect.left - p.rect.left) < SCREEN_WIDTH:
                visible = True
        return visible
#    def is_visible(self, sprite):
#        if sprite.rect.right > self.camera.rect.left and sprite.rect.left < self.camera.rect.right:  
#            return True


    #This method tells the server socket to notify all clients of a collision 
    #(used for interaction between enemies and mario) 
    def notify_collision(self, source_id, side, target_id):
        self.server.sendall("hit:" + str(source_id) + ":" + str(side) + ":" + str(target_id))

    def main_loop(self):
        
        while self.running:            
            self.frame += 1
            if self.frame == SYNC_FREQ:
            
                self.send_game_state() 
                self.frame = 0                               
            if self.frame == int(SYNC_FREQ/2):
                self.send_player_state()
            
            self.i += 1
            self.i = self.i % 2 
  
            self.clock.tick(CLOCK_TICK)
#             self.camera.update()
            for s in self.obt_sprites:
#                if self.is_visible(s):
                s.update(self.clock.get_fps())    
            
            self.check_status()
            self.check_collisions_prot()
    
#            if self.current_iteration < self.pre_period:
#                for s in self.obt_sprites:
#                    left = s.rect.left/32            
#                    if s not in self.dick[left]:
#                        s.append_to_coll_dict(self.dick[left])
##                        print "new sprite in dick"
##                        print len(self.dick[left])
#                self.clock.tick(10000)
#                self.current_iteration += 1
#            else:
#                print "Ended"
            
            
            pygame.display.flip()
#            print self.clock.get_fps()
#            self.handle_events()
#            print self.clock.get_time()

            

        #When out of the loop, we notify those who are waiting on a semaphore
        for s in self.semaphores:
#            print "Releasing"            
            s.release()
   
    def handle_events(self):        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.end()

#===============================================================================
#SERVER GAME CLASS 
#===============================================================================

class ComeTogetherGame(ServerGame):
    
    def __init__(self, server, game_info, game_id, level_name, max_deaths=0):
        ServerGame.__init__(self, server, game_info, game_id, level_name)
        self.max_deaths = max_deaths
        
            
    def check_status(self):
        finished = True
        dead_players = 0
        culprit = ""
        for p in self.players:
            if p.is_dead():
                dead_players += 1
                culprit = p.get_name()        
            if not p.has_won():
                finished = False 
                
        if dead_players > self.max_deaths:
            finished = True
            self.running = False
            for o in self.state_observers:
                o.notify_game_stopped()
            self.server.sendall("lost:" + culprit)
            
    
#     def initialize_camera(self):
#         self.camera = camera.Come_Together_Camera(self.players[self.game_id], self.level.get_size()[0], self)
    
class OnYourOwnGame(ServerGame):
    
    def __init__(self, server, game_info, game_id, level_name, max_deaths=0):
        ServerGame.__init__(self, server, game_info, game_id, level_name)
        self.winners= []    
    
    def check_status(self):
        finished = True
        for p in self.players:
            if not p.has_won() and not p.is_dead():
                finished = False  
        
        if finished:
            self.server.sendall("fin")
    
    def initialize_camera(self):
        self.camera = camera.On_Your_Own_Camera(self.players[self.game_id], self.level.get_size()[0], self)
        
    def notify_win(self, winner):
        self.winners.append(winner)
