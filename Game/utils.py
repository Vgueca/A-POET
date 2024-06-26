from enum import IntEnum

class Action(IntEnum):
    IDLE = 0
    FORWARD = 1
    TURN_LEFT = 2
    TURN_RIGHT = 3

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class CellType(IntEnum):
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
    NOT_VISITED = 11

class Validation(IntEnum):
    VALID = 0
    EMPTY_CELL = 1
    WALL_CELL = 2
    NO_ENERGY = 3

def get_cost(action, cell_type, has_bikini, has_shoes):
    if cell_type == CellType.EMPTY or cell_type == CellType.WALL:
        print("ERROR: EMPTY OR WALL CELL") # RAISE ERROR

    match action:
        case Action.IDLE:
            if cell_type == CellType.CHARGE:
                return -10
            return 0
        case Action.FORWARD:
            match cell_type:
                case CellType.SAND:
                    return 2
                case CellType.WATER:
                    if has_bikini:
                        return 10
                    return 200
                case CellType.GRASS:
                    if has_shoes:
                        return 15
                    return 100
                case CellType.MUD:
                    return 400
                case _:
                    return 1
        case Action.TURN_LEFT | Action.TURN_RIGHT:
            match cell_type:
                case CellType.SAND:
                    return 2
                case CellType.WATER:
                    if has_bikini:
                        return 5
                    return 500
                case CellType.GRASS:
                    if has_shoes:
                        return 1
                    return 3
                case CellType.MUD:
                    return 400
                case _:
                    return 1