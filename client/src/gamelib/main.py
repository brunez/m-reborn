import pygame, os
import game
import client_game
import server_game
import menu 
import data
import sys
import host_menu
import client_menu
import network
import optparse
from pygame.locals import *

class Main:
    def main(self):
        screen_position = parse_args()
        print "Window position: ", screen_position 
        position = [str(screen_position[0]), str(screen_position[1])]
#        os.environ["SDL_VIDEO_CENTERED"] = "1"
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

        #pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()
        pygame.mouse.set_visible(0)
        pygame.display.set_icon(pygame.image.load(data.filepath("bowser1.gif")))
        pygame.display.set_caption("Super Mario Bros (DEMO)")
        self.screen = pygame.display.set_mode((640, 480))
        #Uncomment for full screen
        #pygame.display.toggle_fullscreen()
        
        
        self.options = (["JOIN GAME", lambda: self.join_game(self.screen)],                 
                   ["QUIT GAME", self.quit()])
        
        #=======================================================================
        # Show main menu and retrieve option
        #=======================================================================
        
        while True:
            self.go()
                   
    def go(self):
        #self.show_menu returns the chosen option (join game or quit)            
        option = self.show_menu(self.options)
        
        #Each option has a method linked to it. If it's join game, the method
        #returns info about the game    
        if option != None:         
            info = self.options[option][1]()
        else:
            sys.exit()
        
        #info is a list containing: [game_info (player list), 
        #                            client socket, 
        #                            game id, 
        #                            game mode]
        if info != None:
#             while True:                      
            game_info = info[0]
            client = info[1]            
            game_id = info[2]            
            mode = info[3]
            level_name = info[4]
          
#                print "Initin----------------------------------------------------------------------------"             
            if mode == game.COME_TOGETHER:
                print "Building CT"
                netgame = client_game.ComeTogetherGame(self.screen, client, game_info, game_id, level_name)
            else:
                print "Building OYO"
                netgame = client_game.OnYourOwnGame(self.screen, client, game_info, game_id, level_name)                    
            client.set_game(netgame)                
            clientManager = network.ClientManager(client)
            clientManager.start()
            
            netgame.start()
            clientManager.close()
            clientManager.stop()
            clientManager = None
            netgame = None
            info = self.options[option][1]()
                
        else:
            sys.exit()

    def show_menu(self, options):
        main_menu = menu.Menu(self.screen, options)
        return main_menu.start()           
    
    def join_game(self, screen):        
        joinMenu = client_menu.ClientMenu(screen)
        return joinMenu.start()
                     
    def quit(self):
        sys.exit
    
    
def parse_args():
    usage = """usage: %prog [x] [y]
     """
    parser = optparse.OptionParser(usage)

    _, position = parser.parse_args()
    
    if position:
        x = position[0]
        y = position[1]
    else:
        x = None
        y = None

    return (x, y)


if __name__ == '__main__':        
    m = Main()
    m.main() 
       
