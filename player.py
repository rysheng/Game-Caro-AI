import random
values = ['X', 'O']
value_color = [(255, 0, 0), (0, 0, 255)]

class player(object):
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.color = value_color[values.index(value)]

def creat_player(value):
    return player(0,0, value)