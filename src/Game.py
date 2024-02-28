import numpy as np
import bresenham
from src.Grid import *

class Candidate:

    MOVEMENTS = {
        "u" : (-1, 0),
        "d" : (1, 0),
        "l": (0, -1),
        "r": (0, 1)
    }

    MOVEMENTS_GRAPHIC = {
        "u" : "↑",
        "d" : "↓",
        "l": "←",
        "r":  "→"
    }

    def __init__(self, moves):
       self.moves = moves

    def __getitem__(self, i):
       return Candidate.MOVEMENTS[self.moves[i]]
    
    def __len__(self):
       return len(self.moves)
    
    def __str__(self):
       return str(self.moves)
    
    def get_arrow(self, i):
        return Candidate.MOVEMENTS_GRAPHIC[self.moves[i]]
    


def add_movement(pos , move):
    return (pos[0] + Candidate.MOVEMENTS[move][0], pos[1] + Candidate.MOVEMENTS[move][1])


class Game:

    MOVEMENT_COST = {
        0 : 1.5,
        1 : 0,
        2 : 3,
        3 : 4.5,
        4 : 0,
        5 : 0,
        6 : 0
    }

    def __init__(self, grid, play_pos, obj_pos, enemy_pos):
        self.grid = grid
        self.play_pos = play_pos
        self.obj_pos = obj_pos
        self.enemy_pos = enemy_pos
        self.costs = self.__generate_cost_matrix()
        

        self.DISTANCE_WEIGHT = 1
        self.OBJECTIVE_WEIGHT = 2
        self.START_WEIGHT = 5

    def __generate_cost_matrix(self):
        costs = np.zeros(self.grid.shape)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                costs[i][j] = Game.MOVEMENT_COST.get(self.grid[i][j])

                if self.grid[i][j] in [0, 2, 3] and (i,j) not in self.enemy_pos:
                    for ep in self.enemy_pos:
                        line = self.draw_line(ep, (i,j))
                        crossed = sum([self.grid[el] == 1 for el in line]) > 0
                        if (not crossed):
                            costs[i][j] *= self.__enemy_prob_cost(min(6, len(line)))

                if (i,j) in self.enemy_pos:
                    costs[i][j] *= 100
        return costs


    def __enemy_prob_cost(self, distance):
        if distance == 1:
            return 3
        else:
            return 3 - distance/3

    def draw_line(self, p0, p1):
        return list(bresenham.bresenham(p0[0], p0[1], p1[0], p1[1]))


    
    def get_start(self):
        return self.play_pos
    
    def get_finish(self):
        return self.obj_pos
    
    def get_candidate_path(self, cand):
        return self.grid.generate_path(cand, self.play_pos)
    
    def fitness(self, candidate):
        path = self.grid.generate_path(candidate, self.play_pos)
        fit = 0
        for i in range(1, len(path)):
            cur_pos = path[i]
            old_pos = path[i-1]

            if(cur_pos == old_pos):
                fit += self.DISTANCE_WEIGHT * (2 * self.costs[path[i]])
            else:
                fit += self.DISTANCE_WEIGHT * (self.costs[path[i]])

        obj_distance = sum(abs(np.array(self.obj_pos) - np.array(path[-1]))*1.5)
        str_distance = sum(abs(np.array(self.play_pos) - np.array(path[-1]))*1.5)

        fit += obj_distance * self.OBJECTIVE_WEIGHT
        fit -= str_distance * self.START_WEIGHT


        if (path[-1] == self.obj_pos):
            fit = fit - 10
            return fit, True
        else:
            fit = fit + 30
            return fit, False
        

    def __str__(self):
        data = self.grid.get_printable()
        data[self.play_pos] = "O"
        data[self.obj_pos] = "Y"

        for p in self.enemy_pos:
            data[p] = "Z"

        return print_grid(data)
    
    def review_candidate(self, candidate):
        legal = self.grid.is_legal(candidate, self.play_pos)
        out = self.grid.get_path_printable(candidate, self.play_pos)
        out[self.obj_pos] = "Y"
        for el in self.enemy_pos:
            out[el] = "Z"
        
        fit, complete = self.fitness(candidate)
        print(f"Candidate: {candidate}")
        print(f"Legal:     {legal}")
        print(f"Complete:  {complete}")
        print(f"Fitness:   {fit}")
        print(print_grid(out))

    def print_path(self, candidate):
        return print_grid(self.grid.get_path_printable(candidate, self.play_pos))

    
    def sanitize(self, candidate):
        pos = self.play_pos
        previous_pos = [pos]
        moves = candidate.moves
        final_moves = []
        for move in moves:
            new_pos = self.grid.simulate_move(pos, Candidate.MOVEMENTS[move])
            
            if (new_pos == self.obj_pos):
                final_moves.append(move)
                break

            if new_pos not in previous_pos:
                final_moves.append(move)
                previous_pos.append(new_pos)
                pos = new_pos

        if new_pos == self.obj_pos:
            return Candidate(final_moves)
        else:
            return self.expand_candidate(Candidate(final_moves),100)

    
    def generate_candidate_solution(self, max_lenght):
        pos = self.play_pos
        previous_pos = [pos]
        moves = np.random.choice(["u", "d", "l", "r"], max_lenght)
        final_moves = []
        for move in moves:
            new_pos = self.grid.simulate_move(pos, Candidate.MOVEMENTS[move])
            
            if (new_pos == self.obj_pos):
                final_moves.append(move)
                break

            if new_pos not in previous_pos:
                final_moves.append(move)
                previous_pos.append(new_pos)
                pos = new_pos
        return Candidate(final_moves)

    
    def expand_candidate(self, candidate, max_lenght):

        path = self.get_candidate_path(candidate)
        pos = path[-1]
        previous_pos = path
        final_moves = candidate.moves
        moves = np.random.choice(["u", "d", "l", "r"], max_lenght)
        
        for move in moves:
            new_pos = self.grid.simulate_move(pos, Candidate.MOVEMENTS[move])
            
            if (new_pos == self.obj_pos):
                final_moves.append(move)
                break

            if new_pos not in previous_pos:
                final_moves.append(move)
                previous_pos.append(new_pos)
                pos = new_pos
        return Candidate(final_moves)


    
