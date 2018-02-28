# -*- coding:utf-8 -*-

from piece import Piece

WHITE = 1
BLACK = 0

class IllegalMoveError(Exception):
    pass

class Game():
    
    def __init__(self):
        self.board = [[None for x in range(8)] for x in range(8)]
        self.make_pieces()
        self.player = WHITE
        self.piece_at = lambda (x,y): self.board[x][y]
        self.castle_option = [True, True]
        self.turn = WHITE

    def make_pieces(self):
        pieces= []
        names = ['rook','knight','bishop','king','queen',
          'bishop','knight','rook']
        for i in range(8):
            self.board[i][6] = Piece('pawn', BLACK)
            self.board[i][1] = Piece('pawn', WHITE)
            self.board[i][7] = Piece(names[i], BLACK)
            self.board[i][0] = Piece(names[i], WHITE)
        return pieces

    def castle(self, king_side):
        if not self.castle_option[self.turn]:
            msg = 'Cannot castle, you have already moved your king'
            raise IllegalMoveError(msg)
        row = 7-self.turn*7
        king_x = 3
        rook_x = 0
        king, rook = 2,1
        if not king_side:
            rook_x = 7
            king, rook = 5,4
        if not self.can_castle(king_x, rook_x, row):
            name = 'king'
            if not king_side:
                name = 'queen'
            raise IllegalMoveError("Cannot castle on the "+name+" side") 
        self.board[king][row] = self.board[king_x][row]
        self.board[rook][row] = self.board[rook_x][row]
        self.board[king_x][row] = None
        self.board[rook_x][row] = None

        self.castle_option[self.turn] = False
        self.next_turn()

    def checkable(self, a,b):
        return False

    def can_castle(self, king_x, rook_x, row):
        step = 1
        if king_x > rook_x:
            step = -1
        for i in range(king_x+step, rook_x, step):
            if self.board[i][row] != None:
                return False
            if (self.checkable(i, row)):
                return False
        return True

    def next_turn(self):
        self.turn ^= 1 #0-> 1, 1-> 0

    def hax(self,orig, dest):
        if self.piece_at(orig) is None:
            return
        x,y = dest
        self.board[x][y] = self.piece_at(orig)
        x,y = orig
        self.board[x][y] = None

    def move(self, orig, dest):
        if self.piece_at(orig) is None:
            raise IllegalMoveError('There is no piece there')
        if self.piece_at(orig).color is not self.turn:
            raise IllegalMoveError("The piece at "+orig[0]+","+orig[1]+" is not yours")
        if self.legal_move(orig, dest):
            if self.piece_at(orig).name == 'king':
                self.castle_option[self.turn] = False
            x,y = dest
            self.board[x][y] = self.piece_at(orig)
            self.board[orig[0]][orig[1]] = None
            self.next_turn()
        else:
            raise IllegalMoveError("It's not your turn!")

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


