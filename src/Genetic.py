
import numpy as np
from src.Game import *
from src.Grid import * 

class Population:
    def __init__(self):
        self.p = []

    def __getitem__(self, i):
        return self.p[i][0]
    
    
    def __len__(self):
        return len(self.p)
    
    def get_fitness(self, i):
        return self.p[i][1]

    def __setitem__(self, i, item):
        self.p[i] = item

    def is_complete(self, i):
        self.__getitem__(i)[1]

    def append(self, item):
        self.p.append(item)



class GA:
    def __init__(self, game, selection_probability, tournament_size, mutation_probability, population_size, initial_max_length):
        self.sel_prob = selection_probability
        self.t_size = tournament_size
        self.mutate_prob = mutation_probability
        self.pop_size = population_size
        self.game = game
        self.cumsum = self.__tournament_selection_prob()
        self.population = None
        self.initial_max_length = initial_max_length
        self.generation = 1

    
    def crossover(self, cand1, cand2):
        p1 = np.random.choice(range(1,len(cand1)-1))
        p2 = np.random.choice(range(1,len(cand2)-1))

        new1 = np.append(cand1.moves[0:p1], cand2.moves[p2:])
        new2 = np.append(cand2.moves[0:p2], cand1.moves[p1:])

        return Candidate(list(new1)), Candidate(list(new2))
    
    def mutation(self, candidate):
        moves = candidate.moves
        for i in range(len(moves)):
            if(np.random.uniform() <= self.mutate_prob):
                select = ['u', 'l', 'r', 'd']
                select.remove(moves[i])
                moves[i] = np.random.choice(select)

        return self.game.sanitize(Candidate(moves))

        
   
    def __tournament_selection_prob(self):
        return np.cumsum([self.sel_prob*((1-self.sel_prob)**(r)) for r in range(self.t_size)])
    
    def __choose_candidate_order(self):
        val = np.random.uniform()
        for i in range(self.t_size):
            if val <= self.cumsum[i]:
                return i
        return self.t_size - 1
    
    def _get_candidates_index(self):
        return np.random.choice(range(0, self.pop_size), self.t_size, replace=False, )
    

    def selection_tournament(self):

        candidate_index = self._get_candidates_index()
        winner_index = self.__choose_candidate_order()

        selected_fitness = [self.population.get_fitness(i) for i in candidate_index]
        chosen_value = np.argsort(selected_fitness)[winner_index]

        return candidate_index[chosen_value]


    def generate_initial_population(self):
        self.generation = 1
        self.population = Population()

        for _ in range(self.pop_size):
            cand = self.game.generate_candidate_solution(self.initial_max_length)
            fit, complete = self.game.fitness(cand)
            self.population.append([cand, fit, complete])

    def __getitem__(self, i):
        return self.population[i]
    
    def __len__(self):
        return len(self.population)
    
    def average_fitness(self):
        tot = 0
        for i in range(len(self.population)):
            tot += self.get_fitness(i)
        return tot / len(self)
    
    def get_fitness(self, i):
        return self.population.get_fitness(i)
    
    def get_fittest(self):
        values = [self.population.get_fitness(i) for i in range(len(self.population))]
        ord_index = np.argsort(values)[0:5]
        return ord_index

