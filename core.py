
from random import shuffle


tokens = [1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8,9,-9,10,-10]
tiles = [0,1,2,3,4,5,10,11,12,13,14,20,21,22,23,30,31,32,40,41,50]

def neighbors(tile):
    for x in [tile-10,tile-9,tile-1,tile+1,tile+9,tile+10]:
        if x in tiles:
            yield x
    

class Board:
    def __init__(self,moves):
        self.moves = list(moves)
        #print(self.moves)
        self.avtiles = set(tiles).difference(set(self.moves))
        #print(self.avtiles)
    def get_value(self,tile):
        if tile not in self.moves:
            return 0
        else:
            return tokens[self.moves.index(tile)]
    def get_next(self,x):
        assert x in self.avtiles,"invalid move"
        moves = self.moves[:]
        moves.append(x)
        return Board(moves)
    def get_pos_next(self):
        for x in self.avtiles:
            yield self.get_next(x)
    def is_finished(self):
        return len(self.avtiles) == 1
    def get_random_finish(self,firstmove):
        b = self.get_next(firstmove)
        R = list(b.avtiles)
        shuffle(R)
        
        R = R[:-1]
        R2 = b.moves[:]
        R2.extend(R)
        #print(R2)
        return Board(R2)
    def get_score(self):
        assert self.is_finished()
        s = 0
        for x in neighbors(list(self.avtiles)[0]):
            #print(x,s)
            s += self.get_value(x)
        return s
    def get_move_mcts(self,x,rep):
        s = 0
        for i in range(rep):
            #print(s)
            s += self.get_random_finish(x).get_score()
        #print(s,rep)
        return float(s)/rep
    def best_move(self,rep):
        smax = 0
        bm = None
        for x in self.avtiles:
            s = -self.get_move_mcts(x, rep)
            print(s)
            if bm is None or smax < s:
                s = smax
                bm = x
        return bm



class Tile:
    def __init__(self,tile,mv):
        self.tile = tile
        self.move = mv
        
        
    def get_tile(self):
        return document.getElementById (f'tile_{self.tile}')

    def get_text(self):
        return document.getElementById (f'text_{self.tile}')
    
    def register(self,parent):
        self.parent = parent
        self.get_tile().addEventListener('click',self.fire)
        
    def unregister(self):
        self.get_tile().removeEventListener('click',self.fire)
        
    def fire(self):
        print('move',self.tile)
        self.parent.player_move(self)
        
        
        

class Interact:
    def __init__(self):
        self.cb = Board([])
        self.tiles = {}
        self.rf = 0
        self.lock = False
        
    def perform_move(self,tile):
        
        if len(self.cb.avtiles) <= 1:
            return
        token = tokens[len(self.cb.moves)]
        #print(token)
        if token > 0:
            tile.get_tile().style.fill = 'orange'
        else:
            tile.get_tile().style.fill = 'cyan'
        tile.get_text().innerHTML = str(abs(token))
        tile.get_tile().style.display = 'none'
        tile.get_tile().style.display = 'block'
        self.cb = self.cb.get_next(tile.tile)
        
    def reflow(self):
        self.rf = document.getElementById('blackholeroot').offsetHeight
    def player_move(self,tile):
        print(tile.tile)
        print(tile.move)
        if not tile.tile in self.cb.avtiles:
            return
        if tile.move != len(self.cb.moves):
            return
        if self.lock:
            return
        self.lock = True
        self.perform_move(tile)
        self.perform_move(self.ai_tile())
        self.lock = False
        self.register()
        
    def ai_tile(self):
        m = self.cb.best_move(10000)
        #print(m)
        return self.tiles[m]
        
        
    def register(self):
        for tile in tiles:
            t = Tile(tile,len(self.cb.moves))
            t.register(self)
            self.tiles[tile] = t
            
    def unregister(self):
        for k,v in self.tiles.items():
            print(k,v.tile)
            v.unregister()

        #print(self.tiles)

        
Interact().register()    