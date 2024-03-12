import tkinter as tk

from utils import CellType, Direction

class GameGUI(tk.Tk):
    def __init__(self, initial_game_map, agent_position, agent_orientation):
        super().__init__()
        
        self.title("Game GUI")
        
        self.rows = len(initial_game_map)
        self.cols = len(initial_game_map[0])

        self.create_gui(initial_game_map, agent_position, agent_orientation)
        
    def create_gui(self, game_map, agent_position, agent_orientation):
        self.canvas = tk.Canvas(self, width = self.cols * 50, height = self.rows * 50)
        self.canvas.pack()
        
        self.update_gui(game_map, agent_position, agent_orientation)

    def update_gui(self, game_map, agent_position, agent_orientation):
        self.canvas.delete("all")

        for i in range(self.rows):
            for j in range(self.cols):
                cell_type = game_map[i][j]
                color = self.get_color(cell_type)

                x1, y1 = j * 50, i * 50
                x2, y2 = x1 + 50, y1 + 50

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Draw the agent (triangle)
        agent_x, agent_y = agent_position
        self.draw_triangle(agent_y, agent_x, agent_orientation)
        
        self.update()

    def draw_triangle(self, x, y, orientation):
        length = 30
        width = 15

        direction = {
            Direction.DOWN: (0, 1),
            Direction.RIGHT: (1, 0),
            Direction.UP: (0, -1),
            Direction.LEFT: (-1, 0)
        }[orientation]

        # Compute the triangle vertices
        x1 = x * 50 + 25 - width * direction[1]
        y1 = y * 50 + 25 + width * direction[0]
        x2 = x * 50 + 25 + length * direction[0]
        y2 = y * 50 + 25 + length * direction[1]
        x3 = x * 50 + 25 + width * direction[1]
        y3 = y * 50 + 25 - width * direction[0]

        # Draw the triangle
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="white")

    def get_color(self, cell_type):
        # Map each cell type to a color
        colors = {
            CellType.EMPTY: "black",
            CellType.WALL: "red",
            CellType.STONE: "gray",
            CellType.SAND: "sandy brown",
            CellType.WATER: "blue",
            CellType.GRASS: "green",
            CellType.MUD: "brown",
            CellType.BIKINI: "yellow",
            CellType.SHOES: "purple",
            CellType.CHARGE: "pink",
            CellType.CHECKPOINT: "light blue"
        }
        return colors.get(cell_type)
