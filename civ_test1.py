import pygame as pg
from pygame.locals import *
import random as r

class Nation:
    def __init__(self, controlled, color=(255,0,0), attack=0, defense=0, speed=0):
        self.stats = dict(color=color, attack = attack, defense = defense, speed = speed, can_attack = True)
        self.controlled = controlled
        
    def go(self, board):
        self.controlled = list(dict.fromkeys(self.controlled))
        attack = []
        updated = []
        for xy in self.controlled:
            if board[xy[0]][xy[1]]['can_attack']:
                if xy[0]+1<len(board):
                    if (xy[0]+1,xy[1]) not in self.controlled:
                        if board[xy[0]+1][xy[1]]['defense'] < board[xy[0]][xy[1]]['attack']:
                            attack.append((xy[0]+1,xy[1]))
                if xy[0]>0:
                    if (xy[0]-1,xy[1]) not in self.controlled:
                        if board[xy[0]-1][xy[1]]['defense'] < board[xy[0]][xy[1]]['attack']:
                            attack.append((xy[0]-1,xy[1]))
                if xy[1]+1<len(board[0]):
                    if (xy[0],xy[1]+1) not in self.controlled:
                        if board[xy[0]][xy[1]+1]['defense'] < board[xy[0]][xy[1]]['attack']:
                            attack.append((xy[0],xy[1]+1))
                if xy[1]>0:
                    if (xy[0],xy[1]-1) not in self.controlled:
                        if board[xy[0]][xy[1]-1]['defense'] < board[xy[0]][xy[1]]['attack']:
                            attack.append((xy[0],xy[1]-1))
                        
                if attack == []:
                    board[xy[0]][xy[1]]['can_attack'] = False
                    
                else:
                    for a in attack:
                        if r.randint(0,99) < self.stats['speed']:
                            updated.append((a[0],a[1]))
                    attack = []
        return updated

    def __repr__(self):
        return str(self.stats["color"])+":"+str(len(self.controlled))

class Board:
    def __init__(self, width=100, height=75, buffer=50, size=12):
        self.width = width
        self.height = height
        self.buffer = buffer
        self.buffer_y = buffer
        self.size = size
        self.grid = False
        self.board = self.define_board()
        self.board_width = len(self.board)
        self.board_height = len(self.board[0])
        self.updated = []
        self.red_nation = Nation([], (255, 0, 0), 1, 0, 70)
        self.blue_nation = Nation([], (0, 0, 255), 1, 0, 70)
        self.green_nation = Nation([], (0, 255, 0), 1, 0, 70)
        self.nations = [self.red_nation, self.blue_nation, self.green_nation]

    def reset_board(self):
        self.board = self.define_board()
        for nation in self.nations:
            nation.controlled = []
        self.updated = [(x, y) for x in range(len(self.board)) for y in range(len(self.board[0]))]
        #print(len(self.updated))
        self.update_board()

    def reset_board_color(self):
        self.board = self.define_board()
        for nation in self.nations:
            nation.controlled = []
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                nation = r.choice(self.nations)
                self.update(x, y, nation)
                #nation.controlled.append((x,y))
        self.updated = [(x, y) for x in range(len(self.board)) for y in range(len(self.board[0]))]
        
        #print(len(self.updated))
        self.update_board()

    def define_board(self):
        null_unit = dict(color=(150,150,150), attack=0, defense=0, speed=0, can_attack=True)
        return [[null_unit]*int(self.height) for p in range(int(self.width))]

    def define_size(self, wh):
        self.size = min((wh[0]-self.buffer*2)/self.width, (wh[1]-self.buffer*2)/self.height)
        self.buffer_y = (wh[1]-(self.height*self.size))/2
        
    def draw_board(self):
        pg.draw.rect(win, (150, 150, 150), (self.buffer, self.buffer_y, self.width*self.size, self.height*self.size))
        if self.grid:
            for x in range(self.width+1):
                pg.draw.line(win, (0, 0, 0), (self.buffer+x*self.size, self.buffer_y), (self.buffer+x*self.size, self.height*self.size+self.buffer_y))
            
            for x in range(self.height+1):
                pg.draw.line(win, (0, 0, 0), (self.buffer, self.buffer_y+x*self.size), (self.width*self.size+self.buffer, self.buffer_y+x*self.size))

    def mouse_to_array(self,xy,nation):
        x,y = xy[0], xy[1]
        x-=self.buffer
        y-=self.buffer_y
        
        if x<0 or y<0:
            return None
        
        x = int(x/self.size)
        y = int(y/self.size)
        
        if x>=len(self.board) or y>=len(self.board[0]):
            return None
        
        self.update(x,y,nation)

    def update(self, x, y, nation):
        self.board[x][y] = nation.stats.copy()
        self.updated.append((x,y))
        self.seize(nation)
        self.update_board()

    def update_board(self):
        #print(self.updated)
        for xy in self.updated:
            #print(x, self.updated)
            if self.grid:
                pg.draw.rect(win, self.board[xy[0]][xy[1]]['color'], (self.buffer+xy[0]*self.size+1, self.buffer_y+xy[1]*self.size+1, self.size-1, self.size-1))
            else:
                pg.draw.rect(win, self.board[xy[0]][xy[1]]['color'], (self.buffer+xy[0]*self.size, self.buffer_y+xy[1]*self.size, self.size+1, self.size+1))
            
            if xy[0]+1<len(self.board) and self.board[xy[0]+1][xy[1]]['color'] != self.board[xy[0]][xy[1]]['color']:
                self.board[xy[0]+1][xy[1]]['can_attack'] = True

            if xy[0]>0 and self.board[xy[0]-1][xy[1]]['color'] != self.board[xy[0]][xy[1]]['color']:
                self.board[xy[0]-1][xy[1]]['can_attack'] = True

            if xy[1]+1<len(self.board[0]) and self.board[xy[0]][xy[1]+1]['color'] != self.board[xy[0]][xy[1]]['color']:
                self.board[xy[0]][xy[1]+1]['can_attack'] = True

            if xy[1]>0 and self.board[xy[0]][xy[1]-1]['color'] != self.board[xy[0]][xy[1]]['color']:
                self.board[xy[0]][xy[1]-1]['can_attack'] = True
                
        self.updated = []

    def take_turn(self):
        for nation in self.nations:
            self.updated = nation.go(self.board)
            self.seize(nation)

    def seize(self, nation):
        for xy in self.updated:
            if (xy[0],xy[1]) not in nation.controlled:
                for i in self.nations:
                    if (xy[0],xy[1]) in i.controlled:
                        i.controlled.remove((xy[0],xy[1]))
                nation.controlled.append((xy[0],xy[1]))
                self.board[xy[0]][xy[1]] = nation.stats.copy()
            else:
                self.updated.remove(xy)
        self.update_board()

    def redraw_scene(self,win):
        self.define_size(win.get_size())
        board.draw_board()
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                self.updated.append((x,y))
        self.update_board()
    
pg.init()

win_size = (1600,800)
win=pg.display.set_mode(win_size, RESIZABLE)
pg.display.set_caption("Game")
bg_color = (50,50,50)
win.fill(bg_color)
board = Board()
mouse = pg.mouse
run = True
turns = 0
nation = board.red_nation
#import pdb; pdb.set_trace()
while run:
    pg.time.delay(100)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
            
        elif i.type == pg.VIDEORESIZE:
            win_size = i.size
            win=pg.display.set_mode(win_size, RESIZABLE)
            win.fill(bg_color)
            board.redraw_scene(win)
    k = pg.key.get_pressed()
    
    if mouse.get_pressed()[0]:
        board.mouse_to_array(mouse.get_pos(), nation)

    if k[pg.K_r]:
        nation = board.red_nation

    if k[pg.K_g]:
        nation = board.green_nation 

    if k[pg.K_b]:
        nation = board.blue_nation

    if k[pg.K_0]:
        turns = 0
        board.reset_board()

    if k[pg.K_1]:
        turns = 0
        board.reset_board_color()
        
    if k[pg.K_SPACE]:
        board.take_turn()
        turns+=1
        print(turns)
        print("\t"+str(board.red_nation.__repr__()))
        print("\t"+str(board.green_nation.__repr__()))
        print("\t"+str(board.blue_nation.__repr__()))
        
    if k[pg.K_ESCAPE]:
        run=False

    pg.display.update()

pg.quit()
