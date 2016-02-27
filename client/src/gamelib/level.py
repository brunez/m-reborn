##! /usr/bin/env python
#
#import pygame
#from pygame.locals import *
#
#from data import *
#from sprites import *
#
#TILE_BASE = 16
#TILE_MULT = 2
#TILE_SIZE = TILE_BASE * TILE_MULT
#
#class Level:
#
#    def __init__(self, lvl=1):
#        self.level = pygame.image.load(filepath(("lvl%d.png" % lvl))).convert()
#        self.x = 0
#        self.y = 0
#        self.sprites = pygame.sprite.OrderedUpdates()
#        
#        for y in range(self.level.get_height()):
#            self.y = y
#            for x in range(self.level.get_width()):
#                self.x = x
#                color = self.level.get_at((self.x, self.y))
#                if color == (0, 0, 0, 255):
#                    l=r=False
#                    tile = "middle"
#                    if self.get_at(0, -1) != (0, 0, 0, 255):
#                        tile = "top"
#                    if self.get_at(-1, 0) != (0, 0, 0, 255):
#                        l=True
#                    if self.get_at(1, 0) != (0, 0, 0, 255):
#                        r=True
#                    self.sprites.add(Platform((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                    
#                if color == (0, 19, 127, 255):
#                    l=r=False
#                    tile = "1"
#                    if self.get_at(0, -1) != (0, 19, 127, 255):
#                        tile = "middle"
#                    if self.get_at(-1, 0) != (0, 19, 127, 255):
#                        l=True
#                    if self.get_at(1, 0) != (0, 19, 127, 255):
#                        r=True
#                        
#                    self.sprites.add(Grass((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))    
#
#
#                if color == (109, 127, 63, 255):
#                    l=r=False
#                    tile = "1"
#                    if self.get_at(0, -1) != (109, 127, 63, 255):
#                        tile = "2"
#                    if self.get_at(-1, 0) != (109, 127, 63, 255):
#                        l=True
#                    if self.get_at(1, 0) != (109, 127, 63, 255):
#                        r=True
#
#                    self.sprites.add(Brick((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))    
#
#                if color == (48, 48, 48, 255):
#                    l=r=False
#                    tile = "1"
#                    if self.get_at(0, -1) != (48, 48, 48, 255):
#                        tile = "2"
#                    if self.get_at(-1, 0) != (48, 48, 48, 255):
#                        l=True
#                    if self.get_at(1, 0) != (48, 48, 48, 255):
#                        r=True
#
#                    self.sprites.add(Gray((self.x*TILE_SIZE, self.y*TILE_SIZE), 0, 0))
#                    
#                if color == (255, 200, 0, 255):
#                    self.sprites.add(AirPlatform((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (127, 51, 0, 255):
#                    self.sprites.add(PlatformQ((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (0, 74, 127, 255):
#                    self.sprites.add(Platform_Brick((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (128, 128, 128, 255):
#                    self.sprites.add(Flag((self.x*31.9, self.y*10), 0))
#                if color == (91, 127, 0, 255):
#                    self.sprites.add(Pipe((self.x*TILE_SIZE, self.y*28), 0))
#                if color == (63, 127, 98, 255):
#                    self.sprites.add(Firebowser((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (87, 0, 127, 255):
#                    self.sprites.add(Cloud((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (127, 0, 55, 255):
#                    self.sprites.add(Bush((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (80, 63, 127, 255):
#                    self.sprites.add(Castle((self.x*TILE_SIZE, self.y*22), 0))
#                if color == (255, 233, 127, 255):
#                    self.sprites.add(Hill((self.x*TILE_SIZE, self.y*29), 0))
#                if color == (0, 0, 255, 255):
#                    self.sprites.add(Troopa((self.x*TILE_SIZE + 2, self.y*TILE_SIZE + 4), 0))
#                if color == (0, 255, 255, 255):
#                    self.sprites.add(Goomba((self.x*TILE_SIZE + 1, self.y*TILE_SIZE + 2), 0))
#                if color == (255, 0, 255, 255):
#                    self.sprites.add(Hammer((self.x*TILE_SIZE - 1, self.y*TILE_SIZE - 12), 0))
#                if color ==(255, 106, 0, 255):
#                    self.sprites.add(RedTroopa((self.x*TILE_SIZE + 2, self.y*TILE_SIZE + 4), 0))
#                if color == (76, 255, 0, 255):
#                    self.sprites.add(Cannon((self.x*TILE_SIZE + 1, self.y*29.3 + 4), "cannon") )# 1
#                if color == (63, 73, 127, 255):
#                    self.sprites.add(Cannon((self.x*TILE_SIZE + 1, self.y*24.5  + 4), "cannonbig")) # 1
#                if color == (255, 127, 182, 255):
#                    self.sprites.add(Cannon((self.x*TILE_SIZE + 1, self.y*TILE_SIZE + 2), "smallcannon")) # 1
#                if color == (127, 0, 110, 255):
#                    self.sprites.add(Flower((self.x*(TILE_SIZE+0.5), self.y*28.8 + 2), "flower"))
#                if color == (255, 0, 0, 255):
#                    self.sprites.add(MovingPlatform((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (82, 127, 63, 255):
#                    self.sprites.add(MovingPlatformtwo((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))  
#                if color == (255, 255, 0, 255):
#                    self.sprites.add(Coin((self.x*TILE_SIZE + 4, self.y*TILE_SIZE + 4), 0))
#                if color == (0, 255, 0, 255):
#                    self.sprites.add(Bomb((self.x*31.9, self.y*10), 0))
#                if color == (0, 200, 0, 255):
#                    self.sprites.add(Spring((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (200, 0, 0, 255):
#                    self.sprites.add(Boss((self.x*TILE_SIZE, self.y*TILE_SIZE + 31), 0))
#                if color == (0, 127, 70, 255):
#                    self.sprites.add(MushroomGreen((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (178, 0, 255, 255):
#                    self.sprites.add(PipeBig((self.x*TILE_SIZE, self.y*25), 0))
#                if color == (64, 64, 64, 255):
#                    self.sprites.add(Fence((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (182, 255, 0, 255):
#                    self.sprites.add(Tree1((self.x*TILE_SIZE, self.y*27), 0))
#                if color == (255, 0, 220, 255):
#                    self.sprites.add(Cloud2((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == (72, 0, 255, 255):
#                    self.sprites.add(Rose((self.x*(TILE_SIZE+0.23), self.y*27.8 + 2), "flower2"))
#                if color ==((38, 127, 0, 255)):
#                    self.sprites.add(Tree2((self.x*TILE_SIZE, self.y*29.7), 0))
#                if color ==((0, 127, 127, 255)):
#                    self.sprites.add(Grasstexture((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color ==((255, 0, 110, 255)):
#                    self.sprites.add(Grass1((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color ==((165, 255, 127, 255)):
#                    self.sprites.add(Grass2((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color ==((255, 127, 127, 255)):
#                    self.sprites.add(GrassSprite((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color ==((127, 255, 197, 255)):
#                    self.sprites.add(Wall((self.x*TILE_SIZE, self.y*19), 0))
#                if color == ((214, 127, 255, 255)):
#                    self.sprites.add(Castlebig((self.x*TILE_SIZE, self.y* 6)))
#                if color == ((234, 106, 68, 255)):
#                    self.sprites.add(Lava((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == ((127, 89, 63, 255)):
#                    self.sprites.add(Bridge((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                if color == ((127, 116, 63, 255)):
#                    self.sprites.add(Chain((self.x*TILE_SIZE, self.y*TILE_SIZE), 0))
#                    
#    def get_sprites(self):
#        return self.sprites
#                                       
#    def get_at(self, dx, dy):
#        try:
#            return self.level.get_at((self.x+dx, self.y+dy))
#        except:
#            pass
#            
#    def get_size(self):
#        return [self.level.get_size()[0]*TILE_SIZE, self.level.get_size()[1]*TILE_SIZE]
