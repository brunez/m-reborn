
import socket
import pickle
import network
import game
from ctypes import ARRAY

class Client:
    def __init__(self, server_ip, server_port, menu, host=False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)
#         server_ip = "138.100.154.236"
        self.serv_addr = server_ip, server_port        
        self.menu = menu
        self.isHost = host
        self.game = None
        
    def close(self):
        self.socket.close()
        
    def send(self, data):
#         print "Sending ", data
        pickled = pickle.dumps(data)        
        self.socket.sendto(pickled, self.serv_addr)
#        print "Sent" + data + " to " + str(self.serv_addr)
        
    def set_game(self, game):
        self.game = game
        
        
    #TODO BIG TODO Use split for string analysis
    def receive(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(4096)
#                 print "Client Got " , str(data) ," of type " , str(type(data))
                data = pickle.loads(data)

                #Lists we can receive:
                #    players: A list of network.Avatars representing the players
                #    game_state: A list of objects?? sprites?? representing the game state
                if isinstance(data, list):                    
                    if data[0] == "players":
                        data = data[1:]
#                         print "Received players: ", data 
                        self.menu.set_game_info(data)
                    #The first sync messages can get here before the client
                    #is done constructing, so we check if the game is assigned, just in case    
                    elif data[0] == "sync" and self.game != None:
                        self.game.synchronize(data)
                    elif data[0] == 'ply_sync' and self.game != None:
                        self.game.synchronize_players(data)
                        
                        
                if data[:2] == "id":
                    if not self.isHost: 
                        self.menu.set_id(int(data[3]))
                        self.menu.set_connected(True)
                if data[:5] == "start":
                    mode = int(data[6:7]) 
                    level_name = data[8:]
                    self.menu.set_mode(mode)
                    self.menu.set_ready(True)
                    self.menu.set_level_name(level_name)
                if data[:3] == "act":
                    #action_id = int(data[4])
                    self.game.pay_heed(data) 
                elif data[:3] == "hit":
                    data = data[data.index(":")+1:]
                    source_id = int(data[:data.index(":")]) 
                    data = data[data.index(":")+1:]
                    side = int(data[:data.index(":")])
                    data = data[data.index(":")+1:]
                    target_id = int(data)
                    self.game.note_collision(source_id, side, target_id)
                elif data[:4] == "lost":
                    self.game.lose(data[5:])
                elif data[:4] == "stop":
                    self.game.notify_server_stopped()
                    
            except socket.error:
                break
            
            
   