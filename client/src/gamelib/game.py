#! /usr/bin/env python

import sys, os
import random
import pygame
import sprites
import level_tools
import player
import data
from sprites import *
import platforms
import baddies
from level import *

### Constants
INTRO_DELAY = 1
CLOCK_TICK = 60
# This indicates how brief a tick has to be
# in order to render. This helps avoid lag.
RENDER_THRESHOLD = 20
#This indicates every how many frames the game state is synced
SYNC_FREQ = 60


#ACTIONS
JUMP = str(0)
LEFT = str(1)
RIGHT = str(2)
STOP = str(3)
KEEP_JUMPING = str(4)
STOP_JUMPING = str(5)
#GAME MODES
COME_TOGETHER = 0
ON_YOUR_OWN = 1


#===============================================================================
# GAME BASE CLASS
#===============================================================================
class Game(object):

    #===============================================================================
    # Constructor
    # screen: The drawing surface 
    # server: The network server
    # game_info: The players that have joined the game
    # id: The id of the local player. 0 is the server in a LAN game.
    # 
    #===============================================================================
    def __init__(self, game_info, game_id, level_name):
               
        self.sprites = []
               
        #Sync variables
        self.frame = 0
                
        self.stopped = True
        self.jumping = False
        self.game_id = game_id
        print "My id is ", self.game_id
        self.game_info = game_info
        
        self.highscore = 0
        self.score = 0
        self.lives = 3   
        #This determines which players have arrived         
        self.arrived = []
        self.lost = False
        
            
        self.clock = pygame.time.Clock()
        self.bg = data.load_image("background-2.png")
                
        self.running = True
        self.level_name = level_name
        self.done = False

        #Hum...
        self.i = 0
            
        #=======================================================================
        # Players initialization
        #=======================================================================

        i = 0
        self.players = []
        if game_info[0] == "players":
            game_info.pop(0)
        for p in game_info:            
            plyr = player.Player((0, 0), p.get_name(), i)
            self.players.append(plyr)
            print "Adding player ", str(p), " with id ", plyr.get_object_id()
            print len(self.players) , " players"
            i += 1                     
               
        self.player_collision_group = []
        self.baddie_collision_group = []
        self.mushroom_collision_group = []
        self.colliders = sprites.collider_list
        self.colliders.append(self.players)
               
        self.initialize_images()
        self.initialize_level()
        #TODO quitar old sprites
        #TODO Add deaths, mushrooms, anything left
        self.obt_sprites.add(self.players)
        for s in self.obt_sprites:
            s.add_to_collider_list()
    
        
    #===========================================================================
    # GETTERS AND SETTERS
    #===========================================================================
    
    def get_id(self):
        return self.game_id    
    
    def get_players(self):
        return self.players
    
    def start(self):
        print "Starting..."
#        self.intro_level()
        self.main_loop()    
        return self.done
        
    def end(self):
        self.running = 0
        self.done = True
        
    def initialize_level(self):        
        
        self.booming = False
        self.boom_timer = 0
        self.time = 400
        if self.running:
            
            self.clear_sprites()
            self.level = level_tools.Level_Loader(self.level_name)
            #Here we add the sprites to the main group
            #Children go first because they must be drawn first
            self.obt_sprites = pygame.sprite.OrderedUpdates() #This is an empty list at first
            self._obt_sprites = self.level.get_sprites() #These are the ones created at level.py
            for s in self._obt_sprites:
                for c in s.get_children():
                    self.obt_sprites.add(c)
                                                    
            self.obt_sprites.add(self.level.get_sprites())    
            #===================================================================
            # PROV
            #===================================================================
            self.dick = self.level.get_dick()
            #===================================================================
            # PROV
            #===================================================================
            
            self.game_state_elements = self.level.get_game_state()
            self.sprite_map = self.level.get_sprite_map()
            
            self.initialize_camera()
            self.score -= self.score
            self.highscore = self.highscore
            #play_music("maintheme.ogg")
                            

    def clear_sprites(self):
        for s in self.sprites:
            pygame.sprite.Sprite.kill(s)

    def pay_heed(self, data):
#        print "Action received " + data        
        
        action_id = int(data[4])
        #When player is dead, only synchronize other
#         if not self.players[self.game_id].is_dead() or action_id != self.game_id:
        action = data[5]
        data = data[data.index("_")+1:]
        x = int(data[:data.index("_")])
        data = data[data.index("_")+1:]
        y = int(data)
        pos = (x, y)
        
        #TODO Actual network control        
        if action == JUMP:
            self.players[action_id].jump()                
        elif action == LEFT:
            self.players[action_id].walk(LEFT)                
        elif action == RIGHT:
            self.players[action_id].walk(RIGHT)       
        elif action == STOP:
            self.players[action_id].stop()          
        elif action == KEEP_JUMPING:
            self.players[action_id].keep_jumping()          
        elif action == STOP_JUMPING:
            self.players[action_id].stop_jumping()
                    
        self.players[action_id].set_pos(pos)
#         else:
#             print "Not syncing.  I'm dead."
#        print "My Id: "  + str(self.game_id) + " ActId: " + str(action_id)

    def add_player(self, id):
        self.players.append(player.Player((0, 0))) 
        print "added a player with id " + str(id)
        print self.players


    #abstract
    def check_status(self):
        pass

    #abstract
    def initialize_camera(self):
        pass
    

    def is_visible(self, sprite):
        if sprite.rect.right > self.camera.rect.left and sprite.rect.left < self.camera.rect.right:  
            return True
    def remove_baddie(self, baddie):pass
#        for d in self.dick:
#            if baddie in d:
#                print "removed baddie"
#                d.remove(baddie)
        
        
    #TODO Every collider to one list
    def check_collisions_prot(self):            
        for p in sprites.player_collider_list:
            for s in sprites.player_collision_group:
                if self.is_visible(s):
                    if p.rect.colliderect(s.get_hit_box()): 
                        p.collide(s)

            
        for p in sprites.player_collider_list:
            left = p.rect.left/32                        
            for s in self.dick[left]:
                if p.rect.colliderect(s.get_hit_box()): 
                    p.collide(s)
            if left > 0:
                for s in self.dick[left-1]:
                    if p.rect.colliderect(s.get_hit_box()): 
                        p.collide(s)
            if left < len(self.dick) -1:
                for s in self.dick[left+1]:
                    if p.rect.colliderect(s.get_hit_box()): 
                        p.collide(s)                        
                    
                    
        for b in sprites.baddie_collider_list:
            left = b.rect.left/32            
            for s in self.dick[left]:
                if b.rect.colliderect(s.get_hit_box()): 
                    b.collide(s)
            if left > 0:
                for s in self.dick[left-1]:
                    if b.rect.colliderect(s.get_hit_box()): 
                        b.collide(s)
            if left < len(self.dick) -1:
                for s in self.dick[left+1]:
                    if b.rect.colliderect(s.get_hit_box()): 
                        b.collide(s)   
#        for c in sprites.baddie_collider_list:
#            for s in sprites.baddie_collision_group:                
#                if c.rect.colliderect(s.rect):
#                    c.collide(s)


        
        
    #This method checks if two sprites collide with a certain amount of horizontal overlap     
    def sprites_collide(self, spr1, spr2, h_overlap):
        if spr1.rect.colliderect(spr2.rect):
            if spr1.rect.right > spr2.rect.left + h_overlap and spr1.rect.left < spr2.rect.right - h_overlap:
                return True
            else:
                return False
        else:
            return False  
     
    def initialize_images(self):                
        
        platforms.Grass_Left.images = {"grass-1.png": data.load_image("grass-1.png"), "grass-middle.png": data.load_image("grass-middle.png")}        
#        Brick.images = {"brick1.png": data.load_image("brick1.png"), "brick2.png": data.load_image("brick2.png")}
        
        Bowser_Fireball.image = data.load_image("bowser-fireball1.png")
#        Hammer.left_images = [data.load_image("squidge%d.png" % i) for i in range(1, 3)]
        Cannon.left_images1 = [data.load_image("cannon%d.png" % i) for i in range(1, 3)]
        Cannon.left_images2 = [data.load_image("cannonbig%d.png" % i) for i in range(1, 3)]
        Cannon.left_images4 = [data.load_image("smallcannon%d.png" % i) for i in range(1, 3)]
        Coin.images = [data.load_image("coin%s.png" % i) for i in range(1, 5)]        
        Bomb.image = data.load_image("flagpole.png")
        Bridge.image = data.load_image("bridge.png")
#        BaddieShot.image = data.load_image("shot.png")
        CannonShot.image = data.load_image("cannonbullet1.png")

        Spring.images = [data.load_image("spring1.png"), data.load_image("spring2.png")]        
        
        platforms.Pipe.image = data.load_image("pipe.png")
        Flag.image = data.load_image("flagpole.png")
        Castle.image = data.load_image("castle.png")
        Castlebig.image = data.load_image("castle-big.png")
        Hill.image = data.load_image("hill.PNG")
        Bush.image = data.load_image("bush-1.png")
        Cloud.image = data.load_image("cloud.png")
        Cloud2.image = data.load_image("dobbelclouds.png")
        
        Boss.left_images = [data.load_image("bowser1.png"), data.load_image("bowser2.png"), data.load_image("bowser3.png")]
        Flower.left_images1 = [data.load_image("flower%d.png" % i) for i in range(1, 2)] 
        Greenshroom.image = data.load_image("mushroom-green.png")
        Redshroom.image = data.load_image("mushroom-red.png")
        platforms.Bigpipe.image = data.load_image("pipe-big.png")
        Fence.image = data.load_image("fence.png")
        Tree1.image = data.load_image("tree-1.png")
        Tree2.image = data.load_image("tree-2.png")

        platforms.Grass_Left.image = data.load_image("grass-1.png")
        platforms.Grass_Right.image = data.load_image("grass-2.png")
        platforms.Grass_Base.image = data.load_image("grass-texturesprite.png")
        
        Wall.image = data.load_image("wall-1.png")
        Lava.image = data.load_image("lava.png")
        Chain.image = data.load_image("chain.png")    
    
#    def initialize_collision_groups(self):
#        Player.collision_group = self.player_collision_group
#        Baddie.collision_group = self.baddie_collision_group
#        Mushroom.collision_group = self.mushroom_collision_group

#===============================================================================
#END GAME BASE CLASS 
#===============================================================================
