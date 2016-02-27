'''
Created on Nov 8, 2012

@author: bruno
'''
import jsonpickle
import sprites
import baddies
import platforms
from sprites import *
import pygame

#This dict is used to deserialize the objects contained in the 
#JSON file that represents the level. Each class name is associated
#with the constructor of the corresponding class
constructor_map = dict(Brick=   lambda x, y, e:platforms.Brick_Platform((x*32, y*32), e*2),
           Bush=                lambda x, y, e:sprites.Bush((x*32, y*32), e*2),
           Cloud=               lambda x, y, e:sprites.Cloud((x*32, y*32), e*2),
           Flag=                lambda x, y, e:sprites.Flag((x*32, y*32), e*2),
           Hill=                lambda x, y, e:sprites.Hill((x*32, y*32), e*2),
           Troopa=              lambda x, y, e:baddies.Troopa((x*32, y*32), e*2),
           Greenshroom=         lambda x, y, e:sprites.Greenshroom((x*32, y*32), e*2),
           Redshroom=           lambda x, y, e:sprites.Redshroom((x*32, y*32), e*2),
           Pipe=                lambda x, y, e:platforms.Pipe((x*32, y*32), e*2),
           Bigpipe=             lambda x, y, e:platforms.Bigpipe((x*32, y*32), e*2),
           Brick_Platform=      lambda x, y, e:platforms.Brick_Platform((x*32, y*32), e*2),
           Question_Platform=   lambda x, y, e:platforms.Question_Platform((x*32, y*32), e*2),
           Goomba=              lambda x, y, e:baddies.Goomba((x*32, y*32), e*2))



#class A:
#    def __init__(self, x, y, e):
#        self.x = x
#        self.y = y
#        self.e = e
#
#class B:
#    def __init__(self):        
#        self.b1 = 1        

#This class loads a level
class Level_Loader:

    
    def __init__(self, level):
        
        self.level = level
        self.game_state = []
        self.width = 0
        self.height = 3200
                  
        #TODO The approach used with collisions might be appropriate for this
        #This map associates each class with a plane.
        #Planes are layers used to determine the drawing order of the sprites
        #Sprites in plane 0 are drawn first, sprites in plane 1 are drawn second...
        plane_map = dict(Brick=lambda sprite: self.p2_sprites.add(sprite),
                   Bush=lambda sprite: self.p0_sprites.add(sprite),
                   Cloud=lambda sprite: self.p0_sprites.add(sprite),
                   Flag=lambda sprite: self.p1_sprites.add(sprite),
                   Hill=lambda sprite: self.p0_sprites.add(sprite),
                   Troopa=lambda sprite: self.p3_sprites.add(sprite),
                   Greenshroom=lambda sprite: self.p1_sprites.add(sprite),
                   Redshroom=lambda sprite: self.p1_sprites.add(sprite),
                   Pipe=lambda sprite: self.p2_sprites.add(sprite),
                   Bigpipe=lambda sprite: self.p2_sprites.add(sprite),
                   Brick_Platform=lambda sprite: self.p2_sprites.add(sprite),
                   Question_Platform=lambda sprite: self.p2_sprites.add(sprite),
                   Goomba=lambda sprite: self.p3_sprites.add(sprite))
        
        #This map associates each sprite with a method.
        #It's used to determine if sprites should be considered in
        #game state synchronization
        state_map = dict(Brick=lambda: self.stub(),
                   Bush=lambda x: self.stub(),
                   Cloud=lambda x: self.stub(),
                   Flag= lambda x: self.stub(),
                   Hill= lambda x: self.stub(),
                   Troopa=lambda sprite: self.game_state.append(sprite),
                   Greenshroom=lambda x: self.stub(),
                   Redshroom=lambda x: self.stub(),
                   Pipe=lambda x: self.stub(),
                   Bigpipe=lambda x: self.stub(),
                   Brick_Platform=lambda x: self.stub(),
                   Question_Platform=lambda x: self.stub(),
                   Goomba=lambda sprite: self.game_state.append(sprite))  
                    
        #Decode the level file, which is in JSON format
        jsonpickle.set_encoder_options('simplejson', sort_keys=True)
        
        f = open("../" + self.level, "r")
        r = f.read().replace("py_object", "py/object")
        d = jsonpickle.decode(r) 
        
        #Sprite groups (planes)
        self.sprites = pygame.sprite.OrderedUpdates()
        self.p0_sprites = pygame.sprite.OrderedUpdates()
        self.p1_sprites = pygame.sprite.OrderedUpdates()
        self.p2_sprites = pygame.sprite.OrderedUpdates()
        self.p3_sprites = pygame.sprite.OrderedUpdates()
        

        #Collision groups
        self.player_collision_group = pygame.sprite.Group()
        self.baddie_collision_group = pygame.sprite.Group()
        self.mushroom_collision_group = pygame.sprite.Group()

        #This variable is used to store the width of the level. 
        #When loading the sprites, we just check which one is the rightmost
        rightmost = 0;
        #This dictionary is used to locate sprites with their id's
        self.sprite_map = dict()
        id = 0
        
        #=======================================================================
        # 
        #=======================================================================
        self.mydick = []
        i = 0        
        while i < 264:
            self.mydick.append([])
            i += 1
        #==================================================================
        # 
        #==================================================================
        
        #For every object in the decoded JSON, we invoke the corresponding constructor
        #as per the constructor_map
        #Objects in the level file have the following attributes:
        #c: The name of its class
        #x: Its x position
        #y: Its y position
        #e: Position correction, used for sprites whose size is not a product of the tile size (Not in use right now)
        for o in d:
#            print "Decoding sprite at ", o["x"], ", ", o["y"]
            sprite_ob = constructor_map[o["c"]](o["x"], o["y"], o["e"])
            
            #===================================================================
            # 
            #===================================================================
            sprite_ob.set_dick(self.mydick)                        
            sprite_ob.append_to_coll_dict(self.mydick[o["x"]])          
#            i = 0
#            while i < 10:
#                if o["x"] - i > -1:
#                    sprite_ob.append_to_coll_dict(self.mydick[o["x"]-i])
#                    sprite_ob.append_to_coll_dict(self.mydick[o["x"]+i])
#                i += 1          
#           print "Added shit to ", o["x"]
            #===============================================================
            # 
            #===============================================================
                
#            print "Decoded ", sprite_ob, " at ", sprite_ob.get_position()
            if o["x"]*32 > rightmost:
                rightmost = o["x"]*32
            plane_map[o["c"]](sprite_ob)
            state_map[o["c"]](sprite_ob)
            self.sprite_map[id] = sprite_ob
            sprite_ob.set_object_id(id)
            id += 1
        
        self.set_size(rightmost, self.height)
        
        self.sprites.add(self.p0_sprites)
        self.sprites.add(self.p1_sprites)
        self.sprites.add(self.p2_sprites)
        self.sprites.add(self.p3_sprites)
        
        i = 0
        for s in self.sprites:
            i += 1
            
        print "Level loaded with ", i, " sprites"
        
        self.add_to_collision_groups()

        #Add to collider list
#        for s in self.sprites:
#            s.add_to_collider_list()        
        
        f.close()
        
    def get_sprites(self):
        return self.sprites
    
    
    #===========================================================================
    # PROV
    #===========================================================================
    def get_dick(self):
        return self.mydick
    #===========================================================================
    # PROV
    #===========================================================================
    
    
    
    def get_game_state(self):
        return self.game_state
    
    def get_sprite_map(self):
        return self.sprite_map
    
    def get_size(self):
        return [self.width, self.height]
    
    def set_size(self, width, height):
        self.width = width
        self.height = height
    
    #Here we build the collision groups. The group the sprites are added to
    #depends on what get_collision_groups() yields, which depends on their class
    def add_to_collision_groups(self):
        for s in self.sprites:
            s.add_to_collision_group()
             
    def stub(self):
        pass         
                    
#    def get_player_collision_group(self):
#        return self.player_collision_group
#    
#    def get_baddie_collision_group(self):
#        return self.baddie_collision_group
#    
#    def get_mushroom_collision_group(self):
#        return self.mushroom_collision_group
    
        