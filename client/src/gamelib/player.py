'''
Created on Jan 14, 2013

@author: Runo
'''

import pygame
import data
import game
import platforms
import network
import sprites
import math
from array import array

#PLAYER STATE CONSTANTS
STILL = 0
WALKING_RIGHT = 1
WALKING_LEFT = -1
SLIDING_RIGHT = 2
SLIDING_LEFT = -2
BRAKING_RIGHT = 3
BRAKING_LEFT = -3
JUMPING_RIGHT = 4
JUMPING_LEFT = -4

actions = []

actions.insert(JUMPING_LEFT+4, "jumping left")
actions.insert(BRAKING_LEFT+4, "braking left")
actions.insert(SLIDING_LEFT+4, "sliding left")
actions.insert(WALKING_LEFT+4, "walking left")
actions.insert(4, "Still") 
actions.insert(WALKING_RIGHT+4, "walking right")
actions.insert(SLIDING_RIGHT+4, "sliding right")
actions.insert(BRAKING_RIGHT+4, "braking right")
actions.insert(JUMPING_RIGHT+4, "jumping right")

FACING_LEFT = -1
FACING_RIGHT = 1
THRUSTING_LEFT = -1
THRUSTING_RIGHT = 1
NO_THRUST = 0

SIMPLIFIED_MOVEMENT = True

class Player(sprites.Collidable):

    def __init__(self, pos, name, object_id):
        sprites.Collidable.__init__(self, pos, object_id=object_id)
        self.left_images = []
        for i in self.right_images:
            self.left_images.append(pygame.transform.flip(i, 1, 0))
        self.image = self.right_images[0]
        self.rect = self.image.get_rect(topleft = pos)        
        self.frame = 0
        self.direction = 1
        self.angle = 0
        self.dying = False        
        self.shooting = False
        self.shoot_timer = 0
        self.still_timer = 0
        self.hp = 1
        self.hit_timer = 0
        self.jump_sound = data.load_sound("jump.ogg")
        self.hit_sound = data.load_sound("stomp.ogg")
        self.spring_sound = data.load_sound("jump2.ogg")
        self.springing = False
        self.dx = 1
        self.speed = 0                    
        
        self.won = False
        self.flag = None
#        self.JUMP_KEY = jumpKey

        #Images
        self.win_image = data.load_image("mariowin-%d.png" % (int(self.object_id)+1))
        self.slide_image = data.load_image("mario_slide-%d.png" % (int(self.object_id)+1))
        self.dead_image = data.load_image("mariodie-%d.png" % (int(self.object_id)+1))

        self.thrust = NO_THRUST
        self.state = STILL

        self.name = name
        self.walking = False
        self.braking = False
        self.direction = 1
        self.trying_to_walk = False
        
        self.jump_speed = 0
        self.jump_accel = 0.3
        self.jumping = False
        self.keep_jumping = False
        
        #This is for the dying animation
        self.life = 1
        self.dead_step = -3
        
        self.state_observers = []
        
        #Collision group not in use right now
        self.collision_group = sprites.player_collision_group

    def get_name(self):
        return self.name
    
    def get_hit_box(self):
#         print "RECT: ", self.rect.left, self.rect.top, self.rect.width, self.rect.height
#         print "RECT right: ", self.rect.right
#         print "HB: ", self.rect.left, self.rect.top+5, 26, self.rect.height-5
        return pygame.Rect(self.rect.left, self.rect.top+5, 26, self.rect.height-5)

    def initialize_images(self):
        self.right_images = [data.load_image("mario1-%d.png" % (int(self.object_id)+1)), 
                             data.load_image("mario2-%d.png" % (int(self.object_id)+1)), 
                             data.load_image("mario3-%d.png" % (int(self.object_id)+1)), 
                             data.load_image("mario4-%d.png" % (int(self.object_id)+1)), 
                             data.load_image("mario1-%d.png" % (int(self.object_id)+1)), 
                             data.load_image("mario5-%d.png" % (int(self.object_id)+1)), 
                             data.load_image("mariobr_l.png"), 
                             data.load_image("mariodie-%d.png" % (int(self.object_id)+1))]
        #self.right_images = [data.load_image("mario1-1.png"), data.load_image("mario2-1.png"), data.load_image("mario3-1.png"), data.load_image("mario4-1.png"), data.load_image("mario1-1.png"), data.load_image("mario5-1.png"), data.load_image("mariobr_l.png"), data.load_image("mariodie-1.png")]
        self.image = self.right_images[0]

    def collide(self, sprite):
        if not self.is_dead():
            side = sprites.check_side_rect(self.rect, sprite.get_hit_box())
            self.clamp_off(sprite, side)
            #TODO and local role is server, right?
            if sprite.get_remote_role() == network.ROLE_CLIENT:
                self.notify_collision(side, sprite)
                sprite.take_collision(self, side)
#            if not isinstance(sprite, platforms.Brick_Platform):    
#                print "Collision of", type(self), " with ", type(sprite), " on side ", sprites.COLLISIONS[side]
#                print "My rect: ", self.rect.left, ", ", self.rect.top, ", ", self.rect.width, ", ", self.rect.height
#                print "Sprite's HB: ", sprite.get_hit_box().left, ", ", sprite.get_hit_box().top, ", ", sprite.get_hit_box().width, ", ", sprite.get_hit_box().height
    #        print "Jumping?", self.jumping
    #        print "Jump speed: ", self.jump_speed
                
            #TODO Control bottom collision behaviour here? 
            if side == sprites.BOTTOM_SIDE:
#                if self.get_hit_box().left > sprite.get_hit_box().left and self.get_hit_box().left < sprite.get_hit_box().right-4 or self.get_hit_box().right < sprite.get_hit_box().right and self.get_hit_box().right > sprite.get_hit_box().left+3:   
                self.jumping = False
                        
            if self.rect.bottom <= sprite.rect.top:
                self.jump_speed = min(self.jump_speed, 0)
                #Niapism:
                #When Mario hits something with his bottom, he must stop, but only if he is falling,
                #to prevent weirdness when he jumps right next to a surface.
    #            if self.rect.bottom <= sprite.rect.top:
    #                self.jump_speed = min(self.jump_speed, 0)
    #                
    #            if self.jump_speed is 0:
    #                self.jumping = False
    #                self.springing = False
            
            #If mario top-collides with a prize block, spurt the goodie 
#             if isinstance(sprite, platforms.Question_Platform) or isinstance(sprite, platforms.Brick_Platform):
#                 if side == sprites.TOP_SIDE and self.jump_speed < 0:
#                     sprite.spurt()
        
            
    def take_hit(self):
        print "Mario ", self.object_id, "took hit"
        if self.role == network.ROLE_SERVER:
            print "And I'm a server, so he takes damage"
            if self.hit_timer <= 0:
                self.hit_timer = 20
                self.life -= 1
                if self.life <= 0:
                    self.kill()
                else:
                    self.hit_sound.play()
                            
    def kill(self):
        #pygame.mixer.music.stop()
        self.image = self.dead_image
        sprites.player_collider_list.remove(self)
        self.life = 0
        self.speed = 0
        self.jump_speed = 0        
        
    def shoot(self):
        if not self.shooting and not self.jumping and self.still_timer <= 0:
            self.shooting = True
            self.shoot_timer = 30
            
    def stop_attacking(self):
        self.shooting = False
    
    def get_state(self):
        return self.state
    
    def has_won(self):
        return self.won
    
    def set_won(self, won):
        self.won = won
        
    def add_state_observer(self, observer):
        self.state_observers.append(observer)
    
    def win(self, flag):
        print "I fucking won"
        sprites.player_collider_list.remove(self)
        self.move(30, 0)
        self.flag = flag
        self.speed = 0
        self.jumping = False
        self.jump_speed = 3
        self.won = True
        self.image = self.slide_image
        
        #Notify observers that we won
        for o in self.state_observers:
            o.notify_win(self)
        
    
     
    def get_walking(self): 
        return self.state == WALKING_RIGHT or self.state == WALKING_LEFT

    
    def set_walking(self, value): 
        self.walking = value
        
    def stop(self):        
        if self.state == WALKING_LEFT:
            self.state = SLIDING_LEFT
        elif self.state == WALKING_RIGHT:
            self.state = SLIDING_RIGHT
            
                        
    def jump(self):
#        if not self.jumping and not self.shooting and self.still_timer <= 0:
        self.jump_speed = -9.7
        self.jumping = True
        self.keep_jumping = True
#            self.jump_sound.play()
        self.move(0, -4)
        
    #This method tells mario to jump even higher
    def do_keep_jumping(self):
        if not self.springing:
            self.jump_accel = 0.3
    
    def stop_jumping(self):
        self.jump_accel = 0.6
        self.keep_jumping = False
#        self.jumping = False
                
    def is_jumping(self):
        return self.jumping        
        
    def set_pos(self, pos):
        self.rect.center = pos
    
    def get_pos(self):
        return self.rect.center
    
    def is_dead(self):
        return self.life < 1
    
    
    
    #===========================================================================
    # Movement control
    #===========================================================================
    def walk(self, direction):
#         print "I'm ", self.object_id, ", I'm currently ", actions[self.state+4], " and I  was requested to walk ", direction
#         print "State: ", self.state, " STILL: ", STILL
        if self.state == STILL:
            print "Entered STILL condition"
            self.speed = sprites.INITIAL_SPEED
            print "Setting speed to ", self.speed
            if direction == game.LEFT:   
                print "Direction is ", game.LEFT         
                self.state = WALKING_LEFT
                self.dx = FACING_LEFT
            elif direction == game.RIGHT:
                print "Direction is ", game.RIGHT
                self.state = WALKING_RIGHT
                self.dx = FACING_RIGHT
            else:
                print "Direction is NONE"
        
        elif self.state == WALKING_LEFT:
            if direction == game.RIGHT:
                if SIMPLIFIED_MOVEMENT is True:
                    self.speed = sprites.INITIAL_SPEED
                    self.state = WALKING_RIGHT
                else:
                    self.state = BRAKING_LEFT
                self.thrust = THRUSTING_RIGHT
                
        elif self.state == WALKING_RIGHT:
            if direction == game.LEFT:
                if SIMPLIFIED_MOVEMENT is True:
                    self.speed = sprites.INITIAL_SPEED
                    self.state = WALKING_LEFT
                else:
                    self.state = BRAKING_RIGHT
                self.thrust = THRUSTING_LEFT

        elif self.state == SLIDING_LEFT:
            if direction == game.LEFT:            
                self.state = WALKING_LEFT
#                self.dx = FACING_LEFT
            elif direction == game.RIGHT:
                if SIMPLIFIED_MOVEMENT is True:
                    self.speed = sprites.INITIAL_SPEED
                    self.state = WALKING_RIGHT
                else:
                    self.state = BRAKING_LEFT
                self.thrust = THRUSTING_RIGHT
                self.dx = FACING_RIGHT
                
        elif self.state == SLIDING_RIGHT:
            if direction == game.RIGHT:            
                self.state = WALKING_RIGHT
#                self.dx = FACING_RIGHT
            elif direction == game.LEFT:
                if SIMPLIFIED_MOVEMENT is True:
                    self.speed = sprites.INITIAL_SPEED
                    self.state = WALKING_LEFT
                else:
                    self.state = BRAKING_RIGHT
                self.thrust = THRUSTING_LEFT
                self.dx = FACING_LEFT
    
#         print "I'm ", self.object_id, " and I'm ", actions[self.state+4]
   
    #===========================================================================
    # Update
    #===========================================================================
    def update(self, fps):
#        print "Jumping?", self.jumping
#        print "Jump speed: ", self.jump_speed
        
        #Niapa to adapt to network communication model    
        if not self.is_dead():
            if not self.won:
                self.frame += 1
                self.still_timer -= 1
                self.hit_timer -= 1
                #Remove this from here. Make instance variable.
                top_speed = 3
                
                #When mario jumps, unless the space bar is released, we assume mario 
                #wants to jump higher
                if self.keep_jumping:
                   self.do_keep_jumping() 
                
                if self.jumping:
                    accel = 1.05
#                     initial_speed = 0.7
                else:            
                    accel = 1.08
#                     initial_speed = 0.9
                    
                if self.state == BRAKING_LEFT or self.state == BRAKING_RIGHT:
                    stop_factor = 0.88
                else: 
                    stop_factor = 0.965
                    
                if self.jumping and self.braking:
                    stop_factor = 0.95
                    
                if self.state == WALKING_LEFT:
                    if self.speed < top_speed:
                        self.speed *= accel
                    else:
                        self.speed = top_speed
                    self.direction = -1
                elif self.state == WALKING_RIGHT:
                    if self.speed < top_speed:
                        self.speed *= accel
                    else:
                        self.speed = top_speed
                    self.direction = 1            
                    
                elif self.state == SLIDING_LEFT:
                    if self.speed > 0.5:            
                        self.speed *= stop_factor
                    else:
                        self.speed = 0
                        self.state = STILL 
                    self.direction = -1
                elif self.state == SLIDING_RIGHT:
                    if self.speed > 0.5:            
                        self.speed *= stop_factor
                    else:
                        self.speed = 0
                        self.state = STILL 
                    self.direction = 1    
                    
                #===============================================================
                # BRAKING
                #===============================================================
                elif self.state == BRAKING_LEFT:
                    if self.speed > 0.5:            
                        self.speed *= stop_factor                    
                        if self.speed <= 0.5:
                            self.speed = 0
                        self.state = STILL                                    
                    else:
                        self.speed = 0
                        self.state = STILL                         
                    self.direction = -1
                    
                elif self.state == BRAKING_RIGHT:
                    if self.speed > 0.5:            
                        self.speed *= stop_factor
                        if self.speed <= 0.5:
                            self.speed = 0
                        self.state = STILL                                                    
                    else:                        
                        self.speed = 0
                        self.state = STILL                          
                    self.direction = 1    
                
                #=====================================================
                # JUMPING
                #=====================================================
                if self.jump_speed < 8:
                    self.jump_speed += self.jump_accel
        #        if self.jump_speed > 3:
        #            self.jumping = True        
                
                if self.jumping:
                    if self.dx > 0:
                        self.image = self.right_images[5]
                    if self.dx < 0:
                        self.image = self.left_images[5]
                
                elif self.state == WALKING_LEFT:
                    self.image = self.left_images[1+(int(self.frame/4)%3)]    
                elif self.state == WALKING_RIGHT:
                    self.image = self.right_images[1+(int(self.frame/4)%3)]
        
                        
                elif self.state == SLIDING_LEFT:
                    self.image = self.left_images[1+(int(self.frame/10)%3)]                        
                elif self.state == SLIDING_RIGHT:
                    self.image = self.right_images[1+(int(self.frame/(10))%3)]
                    
                elif self.state == BRAKING_LEFT:
                    self.image = self.left_images[6]  
                elif self.state == BRAKING_RIGHT:
                    self.image = self.right_images[6]
                    
                elif self.state == STILL:
                    if self.dx < 0:
                        self.image = self.left_images[0]
                    elif self.dx > 0:
                        self.image = self.right_images[0]
        
                else:
                    if self.direction > 0:
                        if self.braking:
                            self.image = self.left_images[6]
                        else:
                            self.image = self.right_images[0]
                    if self.direction < 0:
                        if self.braking:
                            self.image = self.right_images[6]
                        else:
                            self.image = self.left_images[0]            
                                
                
                if self.hit_timer > 0:
                    if not self.frame % 2:
                        if self.direction > 0:
                            self.image = self.right_images[2]
                        if self.direction < 0:
                            self.image = self.left_images[2]
        
                
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.top >= 475:
                    pygame.sprite.Sprite.kill(self)
                    
            else:#if won
                if self.rect.bottom > self.flag.get_hit_box().bottom: #If reached the bottom of the flag
                    self.rect.bottom = self.flag.rect.bottom
                    self.image = self.win_image
                    
        else: #if dead        
            #Niapilla
            self.image = self.dead_image    
            self.direction = 0
            self.dead_step += 0.1
            if self.dead_step > 0:
                self.jump_speed = (math.pow(self.dead_step, 2) - 8)
            if self.dead_step > 20:
                pygame.sprite.Sprite.kill(self)                    
       
        self.move(self.speed*self.direction, self.jump_speed) 
        
        #Kill him if he falls from a ledge
        if self.rect.bottom > 480:
            self.kill()    
        
    def add_to_collider_list(self):
        sprites.player_collider_list.add(self)
     