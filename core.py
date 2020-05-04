from random import shuffle

__pragma__('alias', 'S', '$')

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
    def get_score_single(self,flip):
        assert self.is_finished()
        s = 0
        for x in neighbors(list(self.avtiles)[0]):
            #print(x,s)
            if flip:
                s += max(self.get_value(x),0)
            else:
                s += min(self.get_value(x),0)
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
        sz = len(self.avtiles)
        for x in self.avtiles:
            s = self.get_move_mcts(x, rep//sz)
            if bm is None or smax < s:
                smax = s
                bm = x
        #print(bm,smax)
        return bm



        
def get_tile(tile):        
    return S(f'#tile_{tile}')

def get_text(tile):
    return S(f'#text_{tile}')

class Interact:
    def __init__(self):
        self.cb = Board([])
        self.rf = 0
        self.difficulty = 10_000
        
    def perform_move(self,tile):
        
        if len(self.cb.avtiles) <= 1:
            return
        token = tokens[len(self.cb.moves)]
        #print(token)

        get_tile(tile).css( dict(fill= ('orange' if token > 0 else 'cyan')))

        get_text(tile).text(str(abs(token)))
        self.cb = self.cb.get_next(tile)
        
    def player_move(self,event):
        tile = event.data.tile
        print('click')
        self.unregister()
        #print(tile)
        if not tile in self.cb.avtiles:
            return
        self.perform_move(tile)
        self.perform_move(self.ai_tile())
        self.check_finished()
        
    def ai_tile(self):
        m = self.cb.best_move(self.difficulty)
        #print(m)
        return m
    
    def check_finished(self):
        if not self.cb.is_finished():
            return
        for x in tiles:
            if x in list(neighbors(list(self.cb.avtiles)[0])):
                get_text(x).css( {'font-weight':"bold"})
            else:
                get_text(x).css( {'fill':"grey"})
    
    def set_difficulty(self,newval):
        self.difficulty = newval
        
    def register(self):
        for tile in tiles:
            #print(tile)
            get_tile(tile).one('click',{ 'tile': tile },self.player_move)
            
            
    def unregister(self):
        for tile in tiles:
            get_tile(tile).off('click',{ 'tile': tile },self.player_move)


        #print(self.tiles)

        
Interact().register()    