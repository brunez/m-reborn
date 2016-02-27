'''
Created on Mar 29, 2013

@author: bruno
'''

import pygame

def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)



class Camera(object):
    def __init__(self, player, width, game):
        self.player = player        
        self.game = game
        self.rect = pygame.display.get_surface().get_rect()
        self.world = pygame.Rect(0, 0, width, 480)
        self.rect.center = self.player.rect.center
                        
        self.blocked = False
        
    def update(self):
        pass     
            
    def min(self, a, b):
        if a < b:
            return a
        else:
            return b        
    
#     def draw_sprites(self, surf, sprites):        
#         for s in sprites:
#             if s.rect.colliderect(self.rect):
#                 surf.blit(s.image, RelRect(s, self))
                
#The camera is updated differently depending on what mode is activated
#---
#COME_TOGETHER: All the players must be in the same camera frame. 
#If one stays behind, the others can't advance beyond the screen range.
#There's only one camera for every one.
#---
#ON_YOUR_OWN: This is like a race. Every player is on their own,
#so cameras are focused individually.       
#---
#--------------TODO---------------
#MICRO_MACHINES: If one stays behind, he dies.  

class Come_Together_Camera(Camera):
    def update(self):
        leftmost = self.player
        rightmost = self.player      
        i = 0  
        for p in self.game.get_players():
            if p.rect.left < leftmost.rect.left:
                leftmost = p
            if p.rect.right > rightmost.rect.right:
                rightmost = p          
            i += 1    
            
        if leftmost.rect.left <= self.rect.left:
            if not self.blocked: 
                self.blocked = True
        elif self.blocked:
            self.blocked = False
            
        if not self.blocked:
            if rightmost.rect.centerx > self.rect.centerx:
                self.rect.centerx += 3
            elif leftmost.rect.centerx < self.rect.centerx-64:
                self.rect.centerx -= 3
            if self.player.rect.centery > self.rect.centery+64:
                self.rect.centery = self.player.rect.centery-64
            if self.player.rect.centery < self.rect.centery-64:
                self.rect.centery = self.player.rect.centery+64
                
        self.rect.clamp_ip(self.world)        

class On_Your_Own_Camera(Camera):
    def update(self):
        if self.player.rect.centerx > self.rect.centerx+64:
            self.rect.centerx = self.player.rect.centerx-64
        if self.player.rect.centerx < self.rect.centerx-64:
            self.rect.centerx = self.player.rect.centerx+64
        if self.player.rect.centery > self.rect.centery+64:
            self.rect.centery = self.player.rect.centery-64
        if self.player.rect.centery < self.rect.centery-64:
            self.rect.centery = self.player.rect.centery+64
        self.rect.clamp_ip(self.world)
        
        
     