'''
Created on Apr 20, 2013

@author: bruno
'''

import sys
import server
import network
import server_game
import pygame
import game
import threading
from PyQt4 import QtGui
from PyQt4 import QtCore

COME_TOGETHER = 0
ON_YOUR_OWN = 1

class ServerWindow(QtGui.QWidget):
    def __init__(self):
        super(ServerWindow, self).__init__()
        
        #Attributes
        #self.localhost = "192.168.0.192"        
        self.localhost = "127.0.0.1"
        self.host = "138.100.154.236"
        self.host = self.localhost
        self.port = 9999
        
        self.initUI()      
        self.init_attributes()  
                            
    def initUI(self):
        self.setGeometry(100, 300, 800, 600)
        self.setWindowTitle('Super Manuel Server')    
        
        #Buttons
        self.start_server = QtGui.QPushButton('Start Server', self)        
        self.start_server.resize(self.start_server.sizeHint())
        
        self.stop_server = QtGui.QPushButton('Stop server', self)        
        self.stop_server.resize(self.start_server.sizeHint())
        self.stop_server.setEnabled(False)
        
        self.start_game = QtGui.QPushButton('Start game', self)        
        self.start_game.resize(self.start_server.sizeHint())
        self.start_game.setEnabled(False)
        
        self.stop_game = QtGui.QPushButton('Stop game', self)        
        self.stop_game.resize(self.start_server.sizeHint())
        self.stop_game.setEnabled(False)
                     
        
        #Input boxes    
#         self.ip_box = QtGui.QLineEdit()
#         #self.ip_box.resize(50, 15)
#         self.port_box = QtGui.QLineEdit()
#         self.ip_label = QtGui.QLabel("")
#         self.port_label = QtGui.QLabel("Port")
        self.level_box = QtGui.QLineEdit()
        self.level_label = QtGui.QLabel("Level")
        
        #Game modes combo box
        self.game_modes_label = QtGui.QLabel("Game mode")
        self.game_modes = QtGui.QComboBox(self);    
        self.game_modes.addItem("Juntos de la mano");
        self.game_modes.addItem("Marica el ooltimo");
        self.game_modes.resize(self.game_modes.sizeHint())        
        
        #Console
        self.info_box = QtGui.QLabel()
        self.info_box.resize(self.info_box.sizeHint())
        self.info_box.setStyleSheet("background-color:#FFFFFF; border:1px solid gray")
        self.info_box.setMinimumSize(375, 150)
        self.info_box.setMaximumSize(375, 150)
        
        

        # Layout
        self.hbox1 = QtGui.QHBoxLayout()
#         self.hbox1.addWidget(self.ip_label)
#         self.hbox1.addWidget(self.ip_box)        
#         self.hbox1.addWidget(self.port_label)
#         self.hbox1.addWidget(self.port_box)
        self.hbox1.addWidget(self.level_label)
        self.hbox1.addWidget(self.level_box)
        
        self.hbox2 = QtGui.QHBoxLayout()
        self.hbox2.addWidget(self.info_box)
        self.hbox2.addWidget(self.game_modes_label)
        self.hbox2.addWidget(self.game_modes)  
        
              
        self.vbox1 = QtGui.QVBoxLayout()        
        self.vbox1.addLayout(self.hbox1)     
        self.vbox1.addLayout(self.hbox2)           
        self.vbox1.addWidget(self.start_server)
        self.vbox1.addWidget(self.start_game)
        self.vbox1.addWidget(self.stop_server)
        self.vbox1.addWidget(self.stop_game)
        self.setLayout(self.vbox1)

        # Add listeners
        self.connect(self.start_server, QtCore.SIGNAL("clicked()"), self.start_server_clicked)
        self.connect(self.start_game, QtCore.SIGNAL("clicked()"), self.start_game_clicked)
        self.connect(self.stop_server, QtCore.SIGNAL("clicked()"), self.stop_server_clicked)
        self.connect(self.stop_game, QtCore.SIGNAL("clicked()"), self.stop_game_clicked)
        self.connect(self.game_modes, QtCore.SIGNAL("activated()"), self.game_mode_changed)        
        
        self.game = None
        
        self.center()   
        self.show()              
        
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
            self.info_box.setText(self.info_box.text() + p + "\n")
    
    #=======================================================================
    # LISTENERS
    #=======================================================================
    def start_server_clicked(self):      
        
        self.server = server.Server(self.host, self.port, "", self)
        self.serverManager = network.ServerManager(self.server)
        self.serverManager.start()
        self.start_game.setEnabled(True)
        self.start_server.setEnabled(False)
        self.stop_server.setEnabled(True)
        
    def start_game_clicked(self):
        pygame.init()        
        pygame.display.set_mode((640, 480))
        game_info = self.server.get_players()
        
        #TODO Improve
        mode = ""    
        #Set level   
        level = self.level_box.text()
        if level == "":
            level = "level.lvl"    
        if self.game_modes.currentIndex() == COME_TOGETHER: 
            self.game = server_game.ComeTogetherGame(self.server, game_info, 0, level)
            mode = game.COME_TOGETHER
        else:
            self.game = server_game.OnYourOwnGame(self.server, game_info, 0, level)
            mode = game.ON_YOUR_OWN
        

        self.semaphore = threading.Semaphore(0)
        self.game.add_state_observer(self)
        self.game.add_semaphore(self.semaphore)        
        
        self.server.set_game(self.game)
        self.server.start_game(mode, level)
                
        game_manager = GameManager(self.game)
        game_manager.set_game(self.game)
        game_manager.start()
        
        self.start_game.setEnabled(False)
        self.stop_game.setEnabled(True)
        self.stop_server.setEnabled(False)

    def stop_server_clicked(self):        
        print "Stopping server..."
        self.serverManager.close()
        self.serverManager.stop()
        print "Server stopped"
        self.start_game.setEnabled(False)
        self.stop_game.setEnabled(False)
        self.start_server.setEnabled(True)
        self.stop_server.setEnabled(False)
        self.init_attributes()
        self.update_log()
        
        #TODO Temporary...
        sys.exit()    
        
    def stop_game_clicked(self):
        print "Stopping game..."
        self.server.sendall("stop")
        self.game.end()
        print "Waiting for game to do its thing..."
        self.semaphore.acquire(True)
        print "Done"
        pygame.quit()
        print "Game stopped"
        self.set_stop_game_state()
        self.init_attributes()
        
        #TODO Temporary...
        self.serverManager.close()
        self.serverManager.stop()
        sys.exit()    
        
    def game_mode_changed(self):
        self.game_mode = self.game_modes.currentIndex()
            
    def set_stop_game_state(self):
        self.start_game.setEnabled(True)
        self.stop_game.setEnabled(False)
        self.start_server.setEnabled(False)
        self.stop_server.setEnabled(True)
    
    def notify_game_stopped(self):
        self.set_stop_game_state()
        
    def center(self):        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
                
class GameManager(threading.Thread):
    
    def __init__(self, server):  
        threading.Thread.__init__(self)
        self.daemon = True
        
    def set_game(self, game):
        self.game = game
                
    def run(self):        
        self.game.start()
            
    def close(self):
        self.server.close()
        
def main():
    app = QtGui.QApplication(sys.argv)
    s = ServerWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()                