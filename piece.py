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


