class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def make_map(self):
        for x in range(self.width):
            for y in range(self.height):
                if random.randint(0, 100) < 20:
                    self.tiles[x][y].blocked = True
                    self.tiles[x][y].block_sight = True

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[x][y].block_sight:
                    libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    def render_all(self):
        self.render()
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    def clear_all(self):
        for y in range(self.height):
            for x in range(self.width):
                libtcod.console_set_char_background(con, x, y, libtcod.black, libtcod.BKGND_SET)

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False