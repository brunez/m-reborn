#! /usr/bin/env python

import sys
import pygame
import network
import camera
import sprites
import player
import game
import cutscenes
import data
from sprites import *
import platforms


### Constants
INTRO_DELAY = 1
CLOCK_TICK = 60
# This indicates how brief a tick has to be
# in order to render. This helps avoid lag.
RENDER_THRESHOLD = 20
#TODO Not in client. Here it depends on keystrokes.
#This indicates every how many frames the game state is synced
SYNC_FREQ = 60


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


def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)


   
class ClientGame(game.Game):

    #===============================================================================
    # Constructor
    # screen: The drawing surface 
    # client: The network client
    # game_info: The players that have joined the game
    # id: The id of the local player. 0 is the server in a LAN game.
    # 
    #===============================================================================
    def __init__(self, screen, client, game_info, game_id, level_name):
        game.Game.__init__(self, game_info, game_id, level_name)        
        self.sprites = pygame.sprite.OrderedUpdates()
        player.Player.groups = self.sprites
        for c in sprites.baddie_collider_list:
            c.set_role(network.ROLE_CLIENT)
        for p in self.players:
            p.set_role(network.ROLE_CLIENT)

        self.screen = screen

        self.client = client

        self.mario = self.players[self.game_id]

        self.bg = data.load_image("background-2.png")        
                
        self.server_stopped = False
        self.show_names = False
        
#        self.camera = Camera(self.player[self.game_id], self.level.get_size()[0], self.player)
        
        self.font = pygame.font.Font(data.filepath("fonts/font.ttf"), 16)
#         self.heart1 = data.load_image("mario1.png")
#         self.heart2 = data.load_image("mario-life2.png")
#         self.heroimg = data.load_image("mario5.png")
#         self.baddie_sound = data.load_sound("jump2.ogg")
#         self.coin_sound = data.load_sound("coin.ogg")
#         self.up_sound = data.load_sound("1up.ogg")

        self.music = "maintheme.ogg"

        
    def show_death(self):
        ren = self.font.render("YOU DIED", 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 235))
        pygame.display.flip()
        pygame.time.wait(2500)

    def show_end(self):
        #play_music("goal.ogg")
        pygame.time.wait(7500)
        pygame.display.flip()         

  
    def synchronize(self, game_state):
        if game_state[0] == "sync":
            game_state.pop(0)
        for s in game_state:            
            object_id = s.get_object_id()
#            print "Syncing sprite at: ", s.get_position()
#            print "    Life: ", s.get_life()
            self.sprite_map[object_id].set_life(s.get_life())
            self.sprite_map[object_id].set_position(s.get_position())
            self.sprite_map[object_id].set_speed(s.get_speed())
            self.sprite_map[object_id].set_direction(s.get_direction())

    def synchronize_players(self, player_state):
        if player_state[0] == "ply_sync":
            player_state.pop(0)
                
        for p in player_state:
#            print "Synchronizing player ", p.get_object_id(), ", ", p.get_life(), ", ", p.get_position(), ", ", p.get_speed()
            if not self.players[self.game_id].is_dead():
                self.players[p.get_object_id()].set_life(p.get_life())
                self.players[p.get_object_id()].set_position(p.get_position())
                self.players[p.get_object_id()].set_speed(p.get_speed())
                self.players[p.get_object_id()].set_direction(p.get_direction())
                self.players[p.get_object_id()].set_won(p.get_won())

    def is_visible(self, sprite):
        if sprite.rect.right > self.camera.rect.left and sprite.rect.left < self.camera.rect.right:  
            return True

    def note_collision(self, source_id, side, target_id):
        #TODO Try to use sprites_map for players too
        source = self.players[source_id]
        target = self.sprite_map[target_id]
#        print "Noting collision between ", source, " and ", target, " on side ", side
        target.take_collision(source, side)                

    def notify_server_stopped(self):        
        self.server_stopped = True       
        
    def main_loop(self):

        while self.running:
            
            self.frame += 1
            if self.frame == SYNC_FREQ:
                self.frame = 0

            self.clock.tick(CLOCK_TICK)
            self.camera.update()
            for s in self.obt_sprites:
                s.update(self.clock.get_fps())    
                                        
            self.check_collisions_prot()                                 
            self.handle_events()
            
            #This is where drawing is performed. First the background, 
            #then the sprites, then the stats
#            if(self.clock.get_time() < RENDER_THRESHOLD):
            if self.frame % 2 == 0:
                self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640, 0))
                self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640 + 640, 0))
                self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640 - 640, 0))
#                self.camera.draw_sprites(self.screen, self.sprites)
                self.draw_sprites()
#                 self.camera.draw_sprites(self.screen, self.obt_sprites)
                self.draw_stats()
                          
            pygame.display.flip()                        
            
#            print self.clock.get_time()

    def handle_events(self):
        pos_x = self.players[self.game_id].rect.centerx
        pos_y = self.players[self.game_id].rect.centery

        jumping = self.players[self.game_id].is_jumping()
        
        state = self.players[self.game_id].get_state()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.end()
                if e.key == pygame.K_SPACE and not self.players[self.game_id].is_dead() and not self.players[self.game_id].has_won():
                    if not jumping:            
                        self.players[self.game_id].jump()            
                        self.client.send("act:"+ str(self.game_id) +JUMP + "_" + str(pos_x) + "_" + str(pos_y))
            
                #Toggle fullscreen
                if e.key == pygame.K_o:
                    pygame.display.toggle_fullscreen()
                    
                #Toggle names over characters
                if e.key == pygame.K_n:
                    self.show_names = not self.show_names      
                                   
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    self.players[self.game_id].stop_jumping()
                    self.client.send("act:"+ str(self.game_id) +STOP_JUMPING + "_" + str(pos_x) + "_" + str(pos_y))        
                    
        if not self.players[self.game_id].is_dead() and not self.players[self.game_id].has_won():         
            key = pygame.key.get_pressed()               
            if key[pygame.K_a]:
                if state != player.WALKING_LEFT and state != player.BRAKING_RIGHT:
                    self.players[self.game_id].walk(LEFT)
                    self.client.send("act:"+ str(self.game_id) +LEFT + "_" + str(pos_x) + "_" + str(pos_y))
            elif key[pygame.K_d]:
                if state != player.WALKING_RIGHT and state != player.BRAKING_LEFT:     
                    self.players[self.game_id].walk(RIGHT)         
                    self.client.send("act:"+ str(self.game_id) +RIGHT + "_" + str(pos_x) + "_" + str(pos_y))
            else:
                if state == player.WALKING_LEFT or state == player.WALKING_RIGHT:
                    self.players[self.game_id].stop()
                    self.stopped = True
                    self.client.send("act:"+ str(self.game_id) +STOP + "_" + str(pos_x) + "_" + str(pos_y))

    
    def draw_sprites(self):                
        for s in self.obt_sprites:
            if s.rect.colliderect(self.camera.rect):
                self.screen.blit(s.image, RelRect(s, self.camera))
        self.screen.blit(self.players[self.game_id].image, RelRect(self.players[self.game_id], self.camera))
        

    def draw_stats(self):
        ren = self.font.render("FPS: %d" % self.clock.get_fps(), 1, (255, 255, 255))
        self.screen.blit(ren, (511, 41))
        #TODO Only makes sense in CT
        if self.lost:
            self.draw_lost()
            
        if self.server_stopped:
            self.draw_server_stopped()    
        
        if self.show_names:
            self.draw_names()
        
    #TODO Only makes sense in CT
    def draw_lost(self):
        lost_msg = self.font.render("YOU LOST", 1, (255, 255, 255))
        self.screen.blit(lost_msg, (320-lost_msg.get_width()/2, 235))
        if self.culprit != "":
            culprit_msg = self.font.render("BECAUSE OF %s" % self.culprit, 1, (255, 255, 255))
            self.screen.blit(culprit_msg, (320-culprit_msg.get_width()/2, 335))
        pygame.display.flip()
        pygame.time.wait(2500)
        self.running = False
        
    def draw_server_stopped(self):
        lost_msg = self.font.render("SERVER STOPPED", 1, (255, 255, 255))
        self.screen.blit(lost_msg, (320-lost_msg.get_width()/2, 235))        
        pygame.display.flip()
        pygame.time.wait(2500)
        self.running = False

    def draw_names(self):
        for p in self.players:
            player_name = self.font.render(p.name, 1, (255, 255, 255))
            self.screen.blit(player_name, (p.rect.left - self.camera.rect.left, p.rect.bottom-50))

#===============================================================================
# END CLIENT GAME CLASS
#===============================================================================


class ComeTogetherGame(ClientGame):

    def __init__(self, screen, client, game_info, game_id, level_name):
        ClientGame.__init__(self, screen, client, game_info, game_id,level_name)     
        
        #Stores who has lost, so that we can put the blame on them
        self.culprit = ""
    
    def initialize_camera(self):
        self.camera = camera.Come_Together_Camera(self.players[self.game_id], self.level.get_size()[0], self)
            
    def lose(self, culprit=None):        
        self.culprit = culprit
        self.lost = True       
        
class OnYourOwnGame(ClientGame):
    
    def __init__(self, screen, client, game_info, game_id, level_name):
        ClientGame.__init__(self, screen, client, game_info, game_id, level_name)   
        self.winners= []   
        
    def initialize_camera(self):
        self.camera = camera.On_Your_Own_Camera(self.players[self.game_id], self.level.get_size()[0], self)
