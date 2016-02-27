#! /usr/bin/env python

import pygame
import random
import network
import data
import pygame

import math

#COLLISION SIDE CONSTANTS
TOP_SIDE    = 0
RIGHT_SIDE  = 1
BOTTOM_SIDE = 2
LEFT_SIDE   = 3

COLLISIONS = ["TOP", "RIGHT", "BOTTOM", "LEFT"]

#COLLISION GROUPS CONSTANTS
PLAYER = 0
BADDIE = 1
MUSHROOM = 2

#Colliders lists. These lists will contain the sprites that 
#are responsible for checking for collisions
player_collider_list = pygame.sprite.Group()
baddie_collider_list = pygame.sprite.Group()
troopa_collider_list = pygame.sprite.Group()
mushroom_collider_list = pygame.sprite.Group()
collider_list = [baddie_collider_list, troopa_collider_list, mushroom_collider_list]

#Collision groups
player_collision_group = pygame.sprite.Group()
baddie_collision_group = pygame.sprite.Group()
troopa_collision_group = pygame.sprite.Group()
mushroom_collision_group = pygame.sprite.Group()



INITIAL_SPEED = 0.5


#TODO What is this?
def speed_to_side(dx,dy):
    if abs(dx) > abs(dy):
        dy = 0
    else:
        dx = 0
    if dy < 0:
        return 0
    elif dx > 0:
        return 1
    elif dy > 0:
        return 2
    elif dx < 0:
        return 3
    else:
        return 0, 0
    
#This method determines on which side did spr1 collide with spr2 
def check_side(spr1, spr2):
    side = None
    wy = (spr1.rect.width + spr2.rect.width) * (spr1.rect.centery - spr2.rect.centery);
    hx = (spr1.rect.height + spr2.rect.height) * (spr1.rect.centerx - spr2.rect.centerx);
    
    if wy > hx:
        if wy > -hx:
            side = TOP_SIDE
        else:
            side = RIGHT_SIDE
    else:
        if wy > -hx:
            side = LEFT_SIDE
        else:
            side = BOTTOM_SIDE
    return side
    
#This method determines on which side did rect collide with rect2 
def check_side_rect(rect1, rect2):
    side = None
    wy = (rect1.width + rect2.width) * (rect1.centery - rect2.centery);
    hx = (rect1.height + rect2.height) * (rect1.centerx - rect2.centerx);
    
    if wy > hx:
        if wy > -hx:
            side = TOP_SIDE
        else:
            side = RIGHT_SIDE
    else:
        if wy > -hx:
            side = LEFT_SIDE
        else:
            side = BOTTOM_SIDE
    return side
    
    
    
class Collidable(pygame.sprite.Sprite):

    #Fields: TODO
    #id
    def __init__(self, pos, correction = 0, object_id=0, role=network.ROLE_SERVER, remote_role=network.ROLE_SERVER):
        self.object_id = object_id
        self.groups = []
        pygame.sprite.Sprite.__init__(self)    
        self.initialize_images()    
        self.initialize_rect(pos, correction)
        self.collision_group = []
        
        #TODO change field name
        self.collision_groups = []
        self.xoffset = 0
        self.yoffset = 0
        self.children = []
        
        self.jump_speed = 0
        self.jump_accel = 0
        self.speed = 0
        self.jumping = 0
        self.springing = 0
        
        self.life = 0
        self.direction = 0
        
        self.role = role
        self.remote_role = remote_role
            
    #Abstract
    def initialize_images(self):
        pass     
    
    def set_dick(self, dick):
        pass   
    
    def initialize_rect(self, pos, correction = 0):
#        print "Init rect: ", self, " x: ", pos[0], " y: ", pos[1], " corr: ", correction
        pos = (pos[0], pos[1] - correction)
        self.rect = self.image.get_rect(topleft = pos)         


    def is_alive(self):
        return self.life > 0

    def add_child(self, child):
        self.children.append(child)

    def collide(self, spr):
        side = check_side(self, spr)
        self.clamp_off(spr, side)
        
    #This method helps us check if the object is a proxy in the client 
    #and should not perform collision behavior 
    def do_take_collision(self, spr, side):
        if self.role == network.ROLE_SERVER:
            self.take_collision(spr, side)
    
    def take_collision(self, spr, side):
        pass

    def notify_collision(self, side, target):        
        self.game.notify_collision(self.object_id, side, target.get_object_id())
            
    def take_hit(self):
        pass
    
    def take_shell_hit(self):
        pass
    
    def take_spikes(self):
        pass
    
    def bounce(self):
        pass

    def set_default_remote_role(self):
        pass 

    def append_to_coll_dict(self, dic):
        pass
    
    def move(self, dx, dy):

        if dx!=0:
            dx, dummy = self.__move(dx,0)
        if dy!=0:
                dummy, dy = self.__move(0,dy)
        else:
            self.rect.move_ip(dx, dy)
#         return dx, dy
        
    def __move(self,dx,dy):
        oldr = self.rect
        self.rect.move_ip(dx, dy)

        return self.rect.left-oldr.left,self.rect.top-oldr.top   

    #This  method corrects the position of the sprite when it collides with a platform
    #e.g. If you collide with the top of a pipe, your y position doesn't move beyond 
    #the y position of the pipe 
    def clamp_off(self, sprite, side):
        if side == TOP_SIDE:
            self.rect.top = max(sprite.get_hit_box().bottom, self.rect.top)
        if side == RIGHT_SIDE:
            self.rect.right = sprite.get_hit_box().left-1
        if side == BOTTOM_SIDE:
            self.rect.bottom = min(sprite.get_hit_box().top, self.rect.bottom)
        if side == LEFT_SIDE:
            self.rect.left = sprite.get_hit_box().right+1
    

    def draw(self, surf):
        surf.blit(self.image, (self.rect[0]+self.xoffset, self.rect[1]+self.yoffset))
        

    
    def add_to_collider_list(self):
        pass

    def add_to_collision_group(self):
        pass

   
   #============================================================================
   # GETTERS AND SETTERS
   #============================================================================
   
   
    def get_collision_group(self):
        return self.collision_group
    
    def set_collision_group(self, group):
        self.collision_group = group    
        
    def get_position(self):
        return {'x':self.rect.centerx, 'y':self.rect.centery}
    
    def get_speed(self):
        return self.speed
    
    def get_life(self):
        return self.life

    def get_direction(self):
        return self.direction
    
    def set_position(self, pos):
        self.rect.centerx = pos['x']
        self.rect.centery = pos['y']
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_life(self, life):
        self.life = life    

    def set_direction(self, direction):
        self.direction = direction

    def get_collision_groups(self):
        return self.collision_groups

    def get_children(self):
        return self.children

    def get_hit_box(self):
        return self.rect
    
    def set_object_id(self, object_id):
        self.object_id = object_id

    def get_object_id(self):
        return self.object_id    

    def get_role(self):
        return self.role

    def set_role(self, role):
        self.role = role
    
    def get_remote_role(self):
        return self.remote_role

    def set_remote_role(self, role):
        self.remote_role = role
    
    def set_game(self, netgame):
        self.game = netgame
      
        


    
 

class Fence(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        

class Tree1(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        self.on_rignt = False

class Tree2(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        

class Flag(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)                
    
    def initialize_rect(self, pos, correction = 0):
        pos = (pos[0], pos[1] - correction)
        self.rect = self.image.get_rect(topleft = pos)        
    
    def get_hit_box(self):
        return pygame.Rect(self.rect.left+16, self.rect.top, 10, self.rect.height)
        
    def initialize_images(self):
        self.image = data.load_image("flagpole.png")
    
    def get_collision_groups(self):
        return [PLAYER]     
    
    def add_to_collision_group(self):
        player_collision_group.add(self)
        
    def take_collision(self, sprite, side):
        print "Flag took collision"
        sprite.win(self)
        
    def set_default_remote_role(self):
        self.remote_role = network.ROLE_CLIENT 

class Castle(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        

class Castlebig(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        

class Chain(Collidable):
     def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        


class Bush(Collidable):
     def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
                
    
class Bridge(Collidable):
     def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
         

class Cloud(Collidable):
     def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centerx
        self.speed = -00.1
     def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 1
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left
     def update(self, fps):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed
        self.move(-1, self.speed)        

class Cloud2(Collidable):
     def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centerx
        self.speed = -00.1
     def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 1
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left
     def update(self, fps):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed
        self.move(-1, self.speed)              

class Bowser_Fireball(Collidable):
     def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centerx
        self.speed = 0.5
     def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 2
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left
     def update(self, fps):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed
        self.move(-2.9, self.speed)      
                
class Hill(Collidable):
     def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        

        

class Wall(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        

class Lava(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        
        

            
class Spring(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.spring_time = 0
        
        
    def update(self, fps):
        self.image = self.images[0]
        self.spring_time -= 1
        if self.spring_time > 0:
            self.image = self.images[1]
            
    def get_collision_groups(self):
        return [PLAYER]
          
class Stringer(Collidable):
    def __init__(self, pos, dir, id, player):
        Collidable.__init__(self, pos)
        self.rect = self.image.get_rect(center = pos)
        self.move((28-id*12)*dir, 0)
        self.move(54*dir, 0)
        self.player = player
        self.dir = dir
        self.id = id
        if dir < 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.life = 5*id
        self.shoot_sound = data.load_sound("fireball.ogg")
        self.shoot_sound.play()
    def update(self, fps):
        self.rect.center = self.player.rect.center
        self.move((28-self.id*12)*self.dir, 0)
        self.move(54*self.dir, 0)
        self.life -= 1
        if not self.life % 5:
            self.image = pygame.transform.flip(self.image, 0, 0)
        if self.life <= 0:
            self.kill()

#TODO Off with this right/left nonsense. Don't forget about the static initialization
class Flower(Collidable):
    def __init__(self, pos, correction, type="flower"):
        Collidable.__init__(self, pos, correction)
        if type == "flower":
            self.left_images = self.left_images1
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 1
        self.oldy = self.rect.centery
        self.speed = 1
        self.type = type

    def update2(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[int(self.frame/8%2)]
        mult = 1
        if self.type == "flower":
            mult=2
              
# Flower up/down:

    def update(self, fps):
        if self.rect.centery > self.oldy-1:
            self.speed = -self.speed
        if self.rect.centery < self.oldy+110:
            self.speed = -self.speed
        self.move(0, self.speed)
        
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = pygame.Rect(0, 1, 0, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = pygame.Rect(0, 1, 0, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1   

class Cannon(Collidable):
    def __init__(self, pos, correction, type="cannon"):
        Collidable.__init__(self, pos, correction)
        if type == "cannon":
            self.left_images = self.left_images1
        elif type == "cannonbig":
            self.left_images = self.left_images2
        elif type == "smallcannon":
            self.left_images = self.left_images4
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.speed = 1
        self.type = type

    def update(self, fps):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[int(self.frame/2)%2]
        mult = 1
        if self.type == "cannon":
            self.image = self.images[int(self.frame/12)%2]
        elif self.type == "cannonbig":
            self.image = self.images[int(self.frame/12)%2]
        elif self.type == "smallcannon":
            self.image = self.images[int(self.frame/12)%2]
        else:
            self.move(self.speed*mult, 1)

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = pygame.Rect(0, 0, 1, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = pygame.Rect(0, 0, 1, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1        

class CannonShot(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, pos)
        self.rect = self.image.get_rect(bottomleft = pos)
        self.x,self.y=self.rect.topleft
        x = self.x - self.player.rect.centerx
        angle = math.atan(x)
        self.angle = int(265.0 - (angle * 30) / math.pi)
        
    def update(self, fps):
        self.rect.center = (self.x, self.y)
        speed = 2.5
        self.x += math.sin(math.radians(self.angle))*speed

    def get_collision_groups(self):
        return [PLAYER]
    
                               
#class BaddieShot(Collidable):
#    def __init__(self, pos):
#        Collidable.__init__(self, pos, correction)
#        self.rect = self.image.get_rect(center = pos)
#        self.x,self.y=self.rect.center
#        x = self.x - self.player.rect.centerx
#        y = self.y - self.player.rect.centery
#        angle = math.atan2(y, x)
#        self.angle = int(270.0 - (angle * 180) / math.pi)
#    def update(self, fps):
#        self.rect.center = (self.x, self.y)
#        speed = 3
#        self.x += math.sin(math.radians(self.angle))*speed
#        self.y += math.cos(math.radians(self.angle))*speed
#                                      

class Mushroom(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
#        self.rect = self.image.get_rect(topleft = pos)
                
        self.left_to_exit = 32
        self.started = False
        
    def start_moving(self):
        self.started = True

    def update(self, fps):
        if self.started:
            if self.left_to_exit > 0:
                self.move(0, -1)
                self.left_to_exit -= 1
     
    def add_to_collider_list(self):
        mushroom_collider_list.add(self)
        
    def add_to_collision_group(self):
        player_collision_group.add(self)        

class Greenshroom(Mushroom):
    def __init__(self, pos, correction):
        Mushroom.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
   
class Redshroom(Mushroom):
    def __init__(self, pos, correction):
        Mushroom.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
            
                                  
class Coin(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
    def update(self, fps):
        self.frame += 1
        self.image = self.images[int(self.frame/6)%4]
            
class Bomb(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.rect = self.image.get_rect(topleft = pos)
        self.explode_time = 2000
        
        
    def update(self, fps):
        self.explode_time -= 0.5
        

class Explosion(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.image = pygame.Surface((240, 240))
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.image.get_rect(center = pos)
        self.frame = 0
        self.radius = 0
        self.alpha = 255
    def update(self, fps):
        if self.radius >= 120:
            self.alpha -= 20
            if self.alpha <= 0:
                self.kill()
                    
class Boss(Collidable):
    def __init__(self, pos, correction):
        Collidable.__init__(self, pos, correction)
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(bottomleft = pos)
        self.frame = 0
        self.speed = -1
        self.hit_timer = 0
        self.hp = 5
        self.die_time = 0
#        self.dead = False
        
    def kill(self):
        if self.die_time <= 0:
            self.image = pygame.Surface((1, 1))
            self.image.set_alpha(0)
#            self.dead = True
            data.stop_music()
            self.die_time = 200
        
    def hit(self):
        if self.hit_timer <= 0 and self.hp > 0:
            self.hit_timer = 50
            self.hp -= 1
            if self.hp <= 0:
                self.kill()
    
    def update(self, fps):
        self.die_time -= 1
        self.hit_timer -= 1
        if not self.dead:
            if self.speed > 0:
                self.images = self.right_images
            if self.speed < 0:
                self.images = self.left_images
            self.frame += 1
            self.image = self.images[int(self.frame/8)%2]
            if self.hit_timer > 0:
                self.image = self.images[(self.frame/4)%2 + 1]
        mult = 1
        if self.die_time > 0:
            mult = 0
            if not random.randrange(2):
                pos = [0, 0]
                pos[0] = random.randrange(self.rect.left, self.rect.right)
                pos[1] = random.randrange(self.rect.top, self.rect.bottom)
                Explosion(pos)
        self.move(self.speed*mult, 1)
    
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = pygame.Rect(0, 0, 1, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = pygame.Rect(0, 0, 1, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1
