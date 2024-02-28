import numpy as np

CELL_IMAGE = {
    1 : "./assetts/wall.png",
    2 : "./assetts/rough.png",
    3 : "./assetts/obstacle.png",
    4 : "./assetts/rogue.png",
    5 : "./assetts/enemy.png",
    6 : "./assetts/rogue.png"
}


def print_grid(printable_grid):
    output = "   "
    for i in range (1, printable_grid.shape[0] -1):
        output += f" {i}"
    output += "\n"
    for i in range(0, printable_grid.shape[0]):
        if (i > 0) and (i < printable_grid.shape[1] -1):
            output += f"{i}"
        else:
            output += " "
        for j in range(0, printable_grid.shape[1]):
            output += f" {printable_grid[i][j]}"
        if (i > 0) and (i < printable_grid.shape[1] -1):
            output += f" {i}"
        output += "\n"
    output += "   "
    for i in range (1, printable_grid.shape[0] - 1):
        output += f" {i}"
    return output

class Grid:

    PRINT_DATA = {
        0:" ",
        1:"#",
        2:"X",
        3:"T",
        4:"O",
        5:"Z",
        6:"Y"
    }

    def __init__(self, map):
        self.grid = np.array(map)
        self.grid = np.pad(self.grid, pad_width=1, mode='constant', constant_values=1)
        self.size = self.grid.shape[0]
        self.shape = self.grid.shape

    def get_printable(self):
        p = np.empty(self.grid.shape, dtype=str)
        for i in range(self.size):
           for j in range(self.size):
              p[i][j] = Grid.PRINT_DATA[self.grid[i][j]]
        return p
    
    def get(self, i, j):
        return self.grid[i][j]
    
    def __getitem__(self, i):
        return self.grid[i]

    def __str__(self):
        return print_grid(self.get_printable())
    

    def print_path(self, candidate, play_pos):
        return print_grid(self.get_path_printable(candidate, play_pos))


    def simulate_move(self, position, movement):
        new_pos = (position[0] + movement[0], position[1] + movement[1])
        if  self.grid[new_pos] not in [1,5]:
          return new_pos
        else:
          return position
        
    def generate_path(self, candidate, player_pos):
        pos = player_pos
        points = [pos]
        for move in candidate:
            pos = self.simulate_move(pos, move)
            points.append(pos)
        return points
    
    def is_legal(self, candidate, player_pos):
        pos = player_pos

        for move in candidate:
            old = pos
            pos = self.simulate_move(pos, move)
            if old == pos:
                return False
        return True
    
    def get_path_printable(self, candidate, player_pos):
        path = self.generate_path(candidate, player_pos)
        current_printable = self.get_printable()

        for i,point in enumerate(path[:-1]):
            current_printable[point] = candidate.get_arrow(i)

        return current_printable