from enum import Enum

class Action(Enum):
    IDLE = 0
    FORWARD = 1
    TURN_LEFT = 2
    TURN_RIGHT = 3

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class CellType(Enum):
    EMPTY = 0
    WALL = 1
    STONE = 2
    SAND = 3
    WATER = 4
    GRASS = 5
    MUD = 6
    BIKINI = 7
    SHOES = 8
    CHARGE = 9
    CHECKPOINT = 10