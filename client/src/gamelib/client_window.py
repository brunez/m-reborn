'''
Created on May 16, 2013

@author: bruno
'''

import sys
import client
import network
import game
import threading
import client_game
import os
import pygame
import optparse
from PyQt4 import QtGui
from PyQt4 import QtCore

COME_TOGETHER = 0
ON_YOUR_OWN = 1

class ClientWindow(QtGui.QWidget):
    def __init__(self):
        super(ClientWindow, self).__init__()
        
        #Attributes
        self.host = "138.100.154.236"
        self.host = "127.0.0.1"
        self.port = 9999
        self.game = None
        self.client = None
        self.ready = False
        self.connected = False
        self.screen = None
        
        self.initUI()      
        self.init_pygame()
        self.init_attributes()  
                            
    def initUI(self):
        self.setGeometry(700, 300, 800, 600)
        self.setWindowTitle('Super Manuel Client')    
        
        #Buttons
        self.connect_button = QtGui.QPushButton('Connect', self)        
        self.connect_button.resize(self.connect_button.sizeHint())
 
        self.name_box = QtGui.QLineEdit()
        self.name_label = QtGui.QLabel("Name")
  
        #Console
        self.info_box = QtGui.QLabel()
        self.info_box.resize(self.info_box.sizeHint())
        self.info_box.setStyleSheet("background-color:#FFFFFF; border:1px solid gray")
        self.info_box.setMinimumSize(375, 150)
        self.info_box.setMaximumSize(375, 150)
        
        
        # Layout
        self.hbox1 = QtGui.QHBoxLayout()
        self.hbox1.addWidget(self.name_label)
        self.hbox1.addWidget(self.name_box)
        
        self.hbox2 = QtGui.QHBoxLayout()
        self.hbox2.addWidget(self.info_box)   
              
        self.vbox1 = QtGui.QVBoxLayout()        
        self.vbox1.addLayout(self.hbox1)     
        self.vbox1.addLayout(self.hbox2)           
        self.vbox1.addWidget(self.connect_button)
        self.setLayout(self.vbox1)

        # Add listeners
        self.connect(self.connect_button, QtCore.SIGNAL("clicked()"), self.connect_button_clicked)

        
        
        self.center()   
        self.show()              
    
    def init_pygame(self):
        screen_position = parse_args()
        position = [str(screen_position[0]), str(screen_position[1])]
#        os.environ["SDL_VIDEO_CENTERED"] = "1"
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

        #pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()
        pygame.mouse.set_visible(0)                
        self.screen = pygame.display.set_mode((640, 480))
        
    def init_attributes(self):
        self.players = []    
    #===========================================================================
    # LOG
    #===========================================================================
    def add_player(self, data):
        self.players.append(data)        
        self.update_log()
        print "Adding"
        
    def update_log(self):              
        self.info_box.clear()
        for p in self.players:
            self.info_box.setText(self.info_box.text() + p.get_name() + "\n")
    
    #===========================================================================
    # SETTERS
    #===========================================================================
    
    def set_game_info(self, info):
        self.game_info = info
        self.players = info
        self.update_log()
        
    def set_id(self, player_id):
        self.game_id = player_id

    def set_ready(self, ready):
        self.ready = ready        
        
    def set_connected(self, connected):    
        self.connected = connected
        
    def set_mode(self, mode):
        self.mode = mode
        
    def set_level_name(self, level_name):
        self.level_name = level_name
    
    #=======================================================================
    # LISTENERS
    #=======================================================================
    def connect_button_clicked(self):    
#         self.host = self.ip_input.get_content()        
        self.client = client.Client(self.host, 9999, self)
        self.client.send("rtj:"+self.name_box.text())
        self.connected = True
        
        while not self.ready:
            if self.connected:
                self.client.receive()        
                        
        done = False
        while not done:
            print "Ready!"
            if self.mode == game.COME_TOGETHER:
                print "Building CT"
                netgame = client_game.ComeTogetherGame(self.screen, self.client, self.game_info, self.game_id, self.level_name)
            else:
                print "Building OYO"
                netgame = client_game.OnYourOwnGame(self.screen, self.client, self.game_info, self.game_id, self.level_name)
            
            self.client.set_game(netgame)                
            clientManager = network.ClientManager(self.client)
            clientManager.start()
            
            done = netgame.start()
            clientManager.close()
            clientManager.stop()
            clientManager = None
            netgame = None


        
    def center(self):        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
class ConnectionManager(threading.Thread):
    
    def __init__(self, parent, client):  
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent
        self.client = client
        self.client.send("rtj:"+self.name_input.get_content())
        self.connected = True
        self.ready = False
        

        
# class GameLauncher():
#     
#     def __init__(self, server, mode, client_socket, game_info, game_id, level_name):  
#         threading.Thread.__init__(self)
#         self.daemon = True
#         
#         if mode == game.COME_TOGETHER:
#             print "Building CT"
#             netgame = client_game.ComeTogetherGame(self.screen, client_socket, game_info, game_id, level_name)
#         else:
#             print "Building OYO"
#             netgame = client_game.OnYourOwnGame(self.screen, client, game_info, game_id, level_name)    
#                
#         self.client.set_game(netgame)                
#         clientManager = network.ClientManager(client)
#         clientManager.start()
#         
#         netgame.start()
#         clientManager.close()
#         clientManager.stop()
#         clientManager = None
#         netgame = None
#         info = self.options[option][1]()        

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


def main():
    app = QtGui.QApplication(sys.argv)
    c = ClientWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()                