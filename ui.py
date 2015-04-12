# -*- coding:UTF-8 -*-

from game import Game, IllegalMoveError

class InputError(Exception):
    pass

class UI():
    
    def __init__(self, testmode):
        self.game = Game()
        self.testmode = testmode

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
            if not testmode:
                return
            asdf,x,y = cmd.split(' ')
            extract = lambda word: (ord(word[:1])- ord("a"), int(word[1:]) -1)#hax:P
            orig = extract(x)
            dest = extract(y)
            self.game.hax(orig, dest)
            return 
        if 'castle' in cmd: # castle
            if ' ' not in cmd:
                return
            king_side =  cmd.split(' ')[1] == 'king'
            try:
                self.game.castle(king_side)
            except IllegalMoveError as ex:
                print ex
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

        try:
            self.game.move(orig, dest)
        except IllegalMoveError as ex:
            print ex

    def start(self):
        while True:
            self.print_board()
            cmd = raw_input()
            if cmd=="":
                break
            self.user_input(cmd)


