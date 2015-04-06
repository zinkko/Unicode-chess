#!usr/bin/python
# -*- coding:utf-8 -*-


class Piece():
    chars = {
      'pawn':('♙','♟'),
      'knight':('♘','♞'),
      'bishop':('♗','♝'),
      'rook':('♖','♜'),
      'queen':('♕','♛'),
      'king':('♔','♚')
    }
    def init_checks(self):
        diag = lambda (x1,y1), (x2,y2): abs(x1-x2) == abs(y1-y2)
        straight = lambda (x1,y1), (x2,y2): x1 == x2 or y1 == y2
        both = lambda orig, dest: diag(orig, dest) or straight(orig, dest)
        self.movement = {
          'knight': lambda (x1,y1), (x2,y2): (abs(x1-x2),abs(y1-y2)) in [(2,1), (1,2)],
          'rook': straight,
          'bishop': diag,
          'queen': both,  
          'king': lambda (x1,y1), (x2,y2): abs(x1-x2) < 2 and abs(y1-y2) < 2
        }


    def __init__(self, name, color):
        '''Piece("pawn",1,(5,7)) is a white pawn at e7'''
        self.name = name
        self.sign = self.chars[name][color]
        self.color = color
        self.init_checks()
        if name != 'pawn': # pawns will be handled separately
            self.check = self.movement[self.name]
    
    def __str__(self):
        return self.sign


class Game():
    WHITE = 1 #TODO use these 
    BLACK = 0
    
    def __init__(self):
        self.board = [[None for x in range(8)] for x in range(8)]
        self.make_pieces()
        self.player = 1 # 1 is white and 0 is black
        self.piece_at = lambda (x,y): self.board[x][y]
        self.castle_option = [True, True]
        self.turn = 1 

    def make_pieces(self):
        pieces= []
        names = ['rook','knight','bishop','king','queen',
          'bishop','knight','rook']
        for i in range(8):
            self.board[i][6] = Piece('pawn',0)
            self.board[i][1] = Piece('pawn',1)
            self.board[i][7] = Piece(names[i],0)
            self.board[i][0] = Piece(names[i],1)
        return pieces

    def castle(self, king_side):
        if not self.castle_option[self.turn]:
            return
        if not self.path_clear(king_side):
            return
        row = 7-self.turn*7
        king_x = 3
        rook_x = 0
        king, rook = 2,1
        if not king_side:
            rook_x = 7
            king, rook = 5,4
        #
        self.board[king][row] = self.board[king_x][row]
        self.board[rook][row] = self.board[rook_x][row]
        self.board[king_x][row] = None
        self.board[rook_x][row] = None

        self.castle_option[self.turn] = False
        self.turn ^= 1

    def path_clear(self, king_side):
        return True

    def hax(self,orig, dest):
        if self.piece_at(orig) is None:
            return
        x,y = dest
        self.board[x][y] = self.piece_at(orig)
        x,y = orig
        self.board[x][y] = None

    def move(self, orig, dest):
        if self.piece_at(orig) is None:
            return
        if self.piece_at(orig).color is not self.turn:
            print "it's not your turn!"
            return
        if self.legal_move(orig, dest):
            if self.piece_at(orig).name == 'king':
                self.castle_option[self.turn] = False
            x,y = dest
            self.board[x][y] = self.piece_at(orig)
            self.board[orig[0]][orig[1]] = None
            self.turn ^= 1
        else:
            print 'illegal move'

    def legal_move(self, orig, dest):
        to_move = self.piece_at(orig)
        # pawns separately
        if to_move.name == 'pawn':
            return self.pawn_move(orig, dest)
        # legal move if no-one in the way
        if not to_move.check(orig, dest): 
            return False
        # make sure to not capture your own pieces
        nom = self.piece_at(dest)
        if nom is not None and nom.color == to_move.color:
            return False
        if to_move.name in ('knight', 'king'):
            return True
        return self.clear_path(orig, dest)
    
    def clear_path(self, orig, dest):
        x,y = orig
        end_x, end_y = dest

        def approach(a,b):
            if a < b-1:
                return a+1
            elif a > b+1:
                return a-1
            else:
                return a
                
        while abs(x - end_x) > 1 or abs(y - end_y) > 1:
            x = approach(x, end_x)
            y = approach(y, end_y)
            if self.board[x][y] is not None:
                return False
                
        return True

    def pawn_move(self, orig, dest):

        # TODO check for en passant

        forward = 1 #orig-dest when going down
        if self.piece_at(orig).color == 1:
            forward = -1 # up
        if self.piece_at(dest) is not None:
            x_ok = orig[1] - dest[1] == forward
            y_ok = abs(orig[0] - dest[0]) == 1
            return x_ok and y_ok
        
        x_ok = orig[1] - dest[1] == forward
        y_ok = orig[0] == dest[0]
        if orig[1] in (1,6):
            return y_ok and (x_ok or orig[1]-dest[1]==2*forward)
        return x_ok and y_ok


class UI():
    
    def __init__(self):
        self.game = Game()

    def print_board(self):
        board = self.game.board
        x = 'abcdefgh'
        for i in range(7,-1,-1):
            print (i+1),
            for j in range(8):
                nappula = board[j][i]
                if nappula is None:
                    if (i+j)%2!=0:
                        print ' ',
                    else:
                        print '⬛',
                else:
                    print nappula,
            print ''
        print ' ',
        for i in range(8):
            print x[i:i+1],
        print ''

    def user_input(self, cmd):
        if 'hax' in cmd:
            asdf,x,y = cmd.split(' ')
            extract = lambda word: (ord(word[:1])- ord("a"), int(word[1:]) -1)#hax:P
            orig = extract(x)
            dest = extract(y)
            self.game.hax(orig, dest)
            return 
        if 'castle' in cmd: # castle
            king_side =  cmd.split(' ')[1] == 'king'
            self.game.castle(king_side)
            return
        
        if ' ' not in cmd:
            return
        x,y = cmd.split(" ")
        spots =  [a+str(b+1) for a in 'abcdefgh' for b in range(8)]
       
        if not x in spots or not y in spots:
            return
        extract = lambda word: (ord(word[:1])- ord("a"), int(word[1:]) -1)#hax:P
        orig = extract(x)
        dest = extract(y)
        self.game.move(orig, dest)

    def start(self):
        while True:
            self.print_board()
            cmd = raw_input()
            if cmd=="":
                break
            self.user_input(cmd)


if __name__ == '__main__':
    UI().start()
