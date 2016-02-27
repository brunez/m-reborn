'''
Created on Oct 27, 2012

@author: Runo
'''
import socket
import pickle
import network

class Server:
    def __init__(self, host, port, box, parent_menu):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)
        self.socket.bind((host, port))
        self.sent_players = False
        print "Bound to " + host + ", " + str(port)
        
        #The list of hosts that are connected to this game
        self.clients = []
        
        self.used_ids = [0, 0, 0, 0, 0, 0, 0, 0]
        self.box = box
        self.menu = parent_menu
        #To determine if anyone else can join the game
        self.closed = False
        
        #List of Avatars(name, id) representing the players
        #This is sent over the network upon starting
        self.players = ["players"]
        self.game = None
        
    def close(self):        
        self.sendall("stop")
        self.socket.close()
        
    def receive(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(4096)
                data = pickle.loads(data)
                self.process(data, addr)
                
            except socket.error:
                break
    
    def send(self, data, addr):
        self.socket.sendto(pickle.dumps(data), addr)
#        print "Sent " + data + " to", addr
    
    def sendall(self, data):  
        for c in self.clients:
#             print "Sending to " + str(c)
            self.socket.sendto(pickle.dumps(data), c)
            
    def start_game(self, mode, level):
        self.closed = True
        self.sendall("start:" + str(mode) + ":" + level)
    
    def set_game(self, game):
        self.game = game

    def process(self, data, addr):
#        print "Server got ", data

        #Request to join        
        #==========================================================
        if data[:3] == "rtj" and self.closed is False:            
            id = 0
            for i in self.used_ids:
                if i == 0:                    
                    self.used_ids[id] = 1
                    break
                else:
                    id += 1
            if id == 8:
                response = "rejected"
            else:
                #Deprecated. Reemplazar por pintar game_info en menu
                self.menu.add_player(data[4:] + " id: " + str(id))
                response = "id:" + str(id)  
#                if id != 0:              
#                    self.game.add_player(id)
                self.clients.append(addr)
                   
                name = data[4:]
                
                self.players.append(network.Avatar(name, id))
                print "Got here"
                i = 0
                while i < 1000000:
                    i += 1        
                self.send("id:" + str(id), addr)
                self.sendall(self.players)                
        #==========================================================
                
        #A player command was sent by a client 
        if data[:3] == "act":
            self.game.pay_heed(data)
            self.sendall(data)
            
        #The server says: let's roll
        if data == "start":            
            self.start(data)
            
        #The host wants to synchronize the game state
        if data[0] == "sync":
#            print "Sending sync................................................................."
            self.sendall(data)
        
        #The host wants to synchronize the players    
        if data[0] == "ply_sync":
            self.sendall(data)    
#        print "Sending players: ", self.players
        
    def get_players(self):
        return self.players
