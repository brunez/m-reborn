'''
Created on Mar 16, 2013

@author: Runo
'''
            
#===============================================================================
# _______________8888888888_______________
# ______________888888888888______________
# ________@@@@@88888888888888@@@@@________
# ___________8@@888888888888@@8___________
# __________888@@@88888888@@@888__________
# _________88888@@88888888@@88888_________
# ________888881111118881111118888________
# _______88888811@@1188811@@1188888_______
# ______888888811@@1188811@@11888888______
# ______888888811@@1188811@@11888888______
# ______8888888111111888111111888888______
# ______8888888888888888888888888888______
# ______8888888888888888888888888888______
# ______8888888888888888888888888888______
# ______8888888888888888888888888888______
# __________88888111111111188888__________
# __________88888111111111188888__________
# _____________11111111111111_____________
# _____________11111111111111_____________
# _____________111111111111@@@____________
# _____________11111111111@@@@@___________
# _____________@@@111111@@@@@@@@__________
# ____________@@@@@1111@@@@@@@@@__________
# ____________@@@@@11111@@@@@@@___________
# _____________@@@11111111@@@@____________                            BADDIES
#===============================================================================
     
import pygame
import math
import data
import sprites
            
             
class Baddie(sprites.Collidable):    
                        
    def __init__(self, pos, correction):                                                   
        sprites.Collidable.__init__(self, pos, correction)        
        self.right_images = []        
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.left_images
        self.image = self.images[0]
        self.correction = correction
        self.pos = pos
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.speed = 2
        self.jump_speed = 0
        self.fall_accel = 0.3
        self.dead = False
        self.life = 1
        self.time_to_vanish = 60
        self.hit_by_shell = False
        self.dead_step = 1       
        self.coll_dict = []          
        
    def initialize_rect(self, pos, correction = 0):        
        pos = (pos[0], pos[1] - correction)
        self.rect = self.image.get_rect(topleft = pos)    
        
    def get_hit_box(self):        
        return pygame.Rect(self.rect.left+6, self.rect.top+self.correction+6, 20, self.rect.height-6)
    
    def update(self, fps):                  
        
        if self.hit_by_shell:
            self.direction = 0
            self.dead_step += 0.1
            if self.dead_step > 0:
                self.jump_speed = (math.pow(self.dead_step, 2) - 8)
            if self.dead_step > 20:
                pygame.sprite.Sprite.kill(self)
        
        else:
            if self.jump_speed < 8:
                self.jump_speed += self.fall_accel
                
            if self.life > 0:
                if self.speed > 0:
                    self.images = self.right_images
                if self.speed < 0:
                    self.images = self.left_images
                self.frame += 1
                self.image = self.images[int(self.frame/8)%len(self.images)]                
                                       
            else:#if dead
                self.time_to_vanish -= 1
                self.speed = 0
                
            if self.time_to_vanish < 0:
                self.kill()
        
        
             
        #Calculate delta according to fps
#         print "PreSpeed: ", self.speed
#         self.speed *= fps/60
#         print "FPS/60: ", fps/60
#         print "Speed: ", self.speed       

        self.move(self.speed, self.jump_speed)
        
#         print "I'm a baddie and I'm at", self.rect.left
#         print "My speed", self.speed
#         
#         if self.speed < 0:
#             self.speed = -2
#         else:
#              self.speed = 2
            
    def take_collision(self, sprite, side):        
        if side == sprites.BOTTOM_SIDE:
            self.take_hit()
            sprite.jump_speed = -8
        else:
            sprite.take_hit()
              
    def take_hit(self):         
        self.life -= 1
        if self.life is 0:
            self.image = self.dead_image
            sprites.player_collision_group.remove(self)
#            self.game.remove_baddie(self)
            
    def take_shell_hit(self):
        self.hit_by_shell = True
        sprites.baddie_collider_list.remove(self)        
    
    def collide(self, sprite):
        if not isinstance(sprite, Goomba):
            side = sprites.check_side(self, sprite)
            self.clamp_off(sprite, side)
#            print "Collision of", type(self), " with ", type(sprite), " on side ", sprites.COLLISIONS[side]
            if side == sprites.LEFT_SIDE or side == sprites.RIGHT_SIDE:
                #Check that the collision is authentic
                if self.rect.bottom > sprite.rect.top+1:
                    self.speed = -self.speed
    #                print self, " ", self.rect.bottom, " collided with ", sprite, " ", sprite.rect.top, " on the side"
                
            #TODO Control bottom collision behavior here? 
            if side == sprites.BOTTOM_SIDE:
                self.jump_speed = 0
        
    
    def die(self):
#        print "I'm a ", type(self), " and I'm dead."
        self.image = self.dead_image
#        self.dead = True
        sprites.player_collision_group.remove(self)
        self.game.remove_baddie(self)
        
    def get_collision_groups(self):
        return [sprites.PLAYER]
    
    def add_to_collider_list(self):
        sprites.baddie_collider_list.add(self)
        
    def add_to_collision_group(self):
#        self.collision_groups.append(sprites.player_collision_group)
#        self.collision_groups.append(sprites.troopa_collision_group)
        sprites.player_collision_group.add(self)
        sprites.troopa_collision_group.add(self)            

    def set_dick(self, dick):
        pass    
    
    def append_to_coll_dict(self, dic):pass
#        dic.append(self)
#        self.coll_dict.append(dic)
        

class Troopa(Baddie):
    def __init__(self, pos, correction):
        Baddie.__init__(self, pos, correction)        
        self.dead_image = data.load_image("monster3.png")
        self.shell_image = data.load_image("monster3.png")
        
        self.shell_direction = 1
        
        #Death-related variables
        self.life = 2
        
    def initialize_images(self):
        self.left_images = [data.load_image("monster%d.png" % i) for i in range(1, 3)]
        self.image = self.left_images[0]
        
    def collide(self, sprite):
#        print "Troopa collided with ", sprite
        if not isinstance(sprite, Baddie):
            Baddie.collide(self, sprite)
        if self.life == 1:        
            sprite.take_shell_hit()
        
        
    def take_collision(self, sprite, side):
        if side is sprites.BOTTOM_SIDE:
            sprite.jump_speed = -8
            if self.life is 2:        
                self.take_hit()
            elif self.life is 1:
                self.take_off()
                
        else: #if side is not bottom
            if self.speed is 0:
                self.take_off()
            else:
                sprite.take_hit()
                
        
    def take_hit(self):        
        if self.life is 2:
            self.life -= 1            
            self.image = self.shell_image
            self.rect = self.image.get_rect(topleft = (self.rect.left, self.rect.top))            
            self.speed = 0            
        
    def take_off(self):
        self.speed = 8 * self.shell_direction
        
    def update(self, fps):
                                  
        if self.jump_speed < 8:
            self.jump_speed += self.fall_accel
            
        if self.life is 2:
            if self.speed > 0:
                self.images = self.right_images
            if self.speed < 0:
                self.images = self.left_images
            self.frame += 1
            self.image = self.images[int(self.frame/8)%2]            
                     
        elif self.life is 1: #shell
            self.image = self.shell_image
                                   
        elif self.life is 0: #if dead
            self.time_to_vanish -= 1            
            if self.time_to_vanish < 0:
                self.kill()
    
        #Calculate delta according to fps
        self.speed *= fps/60
    
        self.move(self.speed, self.jump_speed)
        
        
    def add_to_collider_list(self):
        Baddie.add_to_collider_list(self)    
        sprites.troopa_collider_list.add(self)
        sprites.troopa_collision_group.remove(self)
        
class Goomba(Baddie):    
    def __init__(self, pos, correction):
        Baddie.__init__(self, pos, correction)
        self.dead_image = data.load_image("slub3.png")

    def initialize_images(self):
        self.left_images = [data.load_image("slub%d.png" % i) for i in range(1, 3)]
        self.image = self.left_images[0]
        
class RedTroopa(Baddie):
    def __init__(self, pos, correction):
        Baddie.__init__(self, pos, correction)
        
    def initialize_images(self):
        self.left_images = [data.load_image("monster-red%d.png" % i) for i in range(1, 3)]
        self.image = self.left_images[0]
        
class Hammer(Baddie):
    def __init__(self, pos, correction):
        Baddie.__init__(self, pos, correction)

class Frank(Baddie):    
    def __init__(self, pos, correction):
        Baddie.__init__(self, pos, correction)
        self.dead_image = data.load_image("slub3.png")

    def initialize_images(self):
        self.left_images = [data.load_image("ysss/frank0%d.png" % i) for i in range(1, 8)]
        self.image = self.left_images[0]
