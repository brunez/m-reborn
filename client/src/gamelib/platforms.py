'''
Created on Mar 16, 2013

@author: Runo
'''
import pygame
import random
import math
import game
import network
import sprites
import data

#===============================================================================
#                       MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
#                       M    ....................  ..M
#                       M  HH;cccccccccccccccccc;MMccM
#                       M  cccc*'          *'ccccccccM
#                       M  cc'                'ncccccM
#                       M  cc     .aMMMMM      MAccccM
#                       M  ccccMMMMMMcccc     aMMccccM
#                       M  cccccccc         .aMM*ccccM
#                       M  cccccccc     .aMMMMP*cccccM
#                       M  ccccccccccMMMMMM*cccccccccM
#                       M  cccccccc'    'ccccccccccccM
#                       M  cccccccc.    .MAccccccccccM
#                       M  ''cccccccc*MMMMPcccccc''ccM
#                       M  MM;cccccccccccccccccc;MMccM
#                       M  ccccccccccccccccccccccccccM
#                       MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM                                       PLATFORMS
#===============================================================================

class Platform(sprites.Collidable):
    def __init__(self, pos, correction):
        sprites.Collidable.__init__(self, pos, correction)                
    
    #TODO Change method name        
    def get_collision_groups(self):
        return [sprites.PLAYER, sprites.BADDIE, sprites.MUSHROOM]
    
    def add_to_collision_group(self):pass
#        sprites.player_collision_group.add(self)
#        sprites.baddie_collision_group.add(self)
#        sprites.mushroom_collision_group.add(self)
            
    def take_collision(self, sprite, side):
        
        if side == sprites.TOP_SIDE:
            #If Mario is falling down right next to a block, a top collision might be detected.
            #To prevent him from stopping for an instant, we only make his jump speed 0
            #if he is not falling (i.e. jump speed < 0)
            sprite.jump_speed = max(self.jump_speed, 0)
        
        if side == sprites.BOTTOM_SIDE:
            if sprite.rect.bottom <= self.rect.top and sprite.rect.left < self.rect.right and sprite.rect.right > self.rect.left:                            
                sprite.jump_speed = min(self.jump_speed, 0)
#                print "Mario: ", sprite.rect.left, ", ", sprite.rect.right, " Platform: ", self.rect.left, ", ", self.rect.right
                #Niapism:
                #When Mario hits something with his bottom, he must stop, but only if he is falling,
                #to prevent weirdness when he jumps right next to a surface.
                
                            
        if sprite.jump_speed is 0:
            sprite.jumping = False
            sprite.springing = False    
      
    def append_to_coll_dict(self, dic):
        dic.append(self)
        
class Rock_Platform(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        
    def initialize_images(self):
        self.image = data.load_image("platform-top.png")

class Air_Platform(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        
    def initialize_images(self):
        self.image = data.load_image("platform-air.png")

class Prize_Platform(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)        
        self.spurting = True
        self.spurt_motion = [-1,1]
        self.spurt_step = 0
        
        #This stack represents the objects in the platform
        #Stack (LIFO) structure
#        self.goodie_stack = []        
    
    def spurt(self):
        self.spurting = True        
        self.pop_goodie()
        
    def pop_goodie(self):
        #If there's anything in the stack...
        if self.children:
            goodie = self.children.pop()
            goodie.start_moving()
        
    def process_spurt(self):
        if self.spurting:
            self.move(0, self.spurt_motion[int(self.spurt_step/15)%2])
            self.spurt_step += 1
            if self.spurt_step == 30:
                self.spurting = False
                self.spurt_step = 0


class Gray_Brick_Platform(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        self.image = self.images["gray1.png"]
                



class Question_Platform(Prize_Platform):
    def __init__(self, pos, correction):
        Prize_Platform.__init__(self, pos, correction)
        self.image = self.images[0]
        
        self.frame = 0
#        self.add_child(Redshroom(self.rect.topleft, correction))

    def initialize_images(self):
        self.images = [data.load_image("platform-q%s.png" % i) for i in range (1, 4)]
        self.image = self.images[0]

    def update(self, fps):
        self.frame += 1
        self.image = self.images[int(self.frame/39%3)]
        self.process_spurt()
        
        
class Brick_Platform(Prize_Platform):
    def __init__(self, pos, correction):
        Prize_Platform.__init__(self, pos, correction)
        
    def initialize_images(self):
        self.image = data.load_image("platform-brick.png")
    
    def update(self, fps):
        self.process_spurt()   


class Pipe(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        
        
        

class Bigpipe(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        
    


class Grass_Left(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        
        
        

class Grass_Right(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        
        
        

class Grass_Base(Platform):
    def __init__(self, pos, correction):
        Platform.__init__(self, pos, correction)
        
         
                
class Spikes(sprites.Collidable):
    def __init__(self, pos, correction):
        sprites.Collidable.__init__(self, pos, correction)
        
  