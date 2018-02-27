#!/usr/bin/python
# -*- coding:utf-8 -*-

from ui import UI

from sys import argv

if __name__ == '__main__':
    testmode = len(argv) > 1 and argv[1] == 'test'
    UI(testmode).start()
