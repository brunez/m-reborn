import threading

ROLE_CLIENT = 0
ROLE_SERVER = 1

class Avatar:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    
class ServerManager(threading.Thread):
    
    def __init__(self, server):  
        threading.Thread.__init__(self)       
        self.daemon = True
        self.server = server            
        self.running = True
            
    def run(self):        
        while self.running:                  
            self.server.receive()
            
    def close(self):
        self.server.close()
        
    def stop(self):
        self.running = False

class ClientManager(threading.Thread):
    
    def __init__(self, client):  
        threading.Thread.__init__(self)       
        self.daemon = False
        self.client = client
        self.running = True    
    def run(self):        
        while self.running:
            self.client.receive()
            
    def close(self):
        self.client.close()
        
    def stop(self):
        self.running = False
        
class HostGameManager(threading.Thread):
    
    def __init__(self, game):  
        threading.Thread.__init__(self)       
        self.daemon = True
        self.game = game    
    def run(self):        
        self.game.start()
            
    def close(self):
        pass
           

class SpriteState:
    def __init__(self, life, pos, speed, direction, object_id):
        self.pos = pos
        self.life = life
        self.speed = speed
        self.direction = direction        
        self.object_id = object_id
        
    def get_position(self):
        return self.pos
    
    def get_speed(self):
        return self.speed
    
    def get_life(self):
        return self.life

    def get_direction(self):
        return self.direction
    
    def get_object_id(self):
        return self.object_id
    
    def set_position(self, pos):
        self.pos = pos
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_life(self, life):
        self.life = life

    def set_direction(self, direction):
        self.direction = direction
        
    def set_object_id(self, object_id):
        self.object_id = object_id
        
class PlayerState:
    def __init__(self, life, pos, speed, direction, won, object_id):
        self.pos = pos
        self.life = life
        self.speed = speed
        self.direction = direction
        self.won = won        
        self.object_id = object_id
        
    def get_position(self):
        return self.pos
    
    def get_speed(self):
        return self.speed
    
    def get_life(self):
        return self.life

    def get_direction(self):
        return self.direction
    
    def get_won(self):
        return self.won
    
    def get_object_id(self):
        return self.object_id
    
    def set_position(self, pos):
        self.pos = pos
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_life(self, life):
        self.life = life

    def set_direction(self, direction):
        self.direction = direction
    
    def set_won(self, won):
        self.won = won
        
    def set_object_id(self, object_id):
        self.object_id = object_id