import src.Examples as Exp
from src.Game import *
from src.Genetic import *


if __name__== "__main__":
   
    m = Exp.EXAMPLE_MAP_2

    GRID = Grid(m['map'])
    PLAY_POS = m['p']
    OBJ_POS = m['o']
    ENEMY_POS = m['e']
    MAC_LENGHT = 25
    TOURN_SIZE = 5
    SELECTION_PROB = 0.80
    MUTATION_PROB  = 0.15
    POP_SIZE = 50
    INITIAL_LENGTH = 100
    MAX_GENERATION = 100


    game = Game(GRID, PLAY_POS, OBJ_POS, ENEMY_POS)

    print("\n === MAPPA DI GIOCO CARICATA ==================================\n")
    print(game)
    print("\n ==============================================================\n")

   

    np.random.seed(None)

    genetic = GA(game, SELECTION_PROB, TOURN_SIZE, MUTATION_PROB, POP_SIZE, INITIAL_LENGTH)


    print("=== POPOLAZIONE GENERAZIONE 0 ==================================\n")
    


    genetic.generate_initial_population()

    print("Average Fitness Generazione:",genetic.average_fitness())
    print("Miglior candidato generazione 0:")

    index = genetic.get_fittest()[0]
    game.review_candidate(genetic[index])

    print("\n================================================================\n")


    best_fitness = []
    best_fitness.append(genetic.population.get_fitness(index))
    
    # MAIN LOOP

    print("\n === INIZIO APPRENDIMENTO ================================== \n")
    print(f"GEN {0:03d} | BEST {genetic.get_fitness(index):+04.3f}")


    for gen in range(0,MAX_GENERATION):
        new_pop = Population()
        for i in range(0, int(POP_SIZE / 2)):
            
            chosen1 = genetic.selection_tournament()
            chosen2 = genetic.selection_tournament()

            n1, n2 = genetic.crossover(genetic[chosen1], genetic[chosen2])

            n1 = genetic.mutation(n1)
            n2 = genetic.mutation(n2)
    
            f1, c1 = game.fitness(n1)
            f2, c2 = game.fitness(n2)

            new_pop.append([n1, f1, c1])
            new_pop.append([n2, f2, c2])

            if((gen % 10) == 0):
                genetic.mutate_prob -= 0.05


        genetic.population = new_pop
        index = genetic.get_fittest()[0]
        print(f"GEN {gen+1:03d} | BEST {genetic.get_fitness(index):+04.3f}")
        best_fitness.append(genetic.population.get_fitness(index))


    print("\n================================================================\n")

    print("\n === SOLUZIONE TROVATA ================================== \n")

    index = genetic.get_fittest()[0]
    game.review_candidate(genetic[index])
  


    import matplotlib.pyplot as plt

    plt.plot(range(len(best_fitness)), best_fitness, label="Migliore Fitness nella popolazione")
    plt.legend()
    plt.xlabel("Generazione")
    plt.ylabel("Fitness")
    plt.title("Analisi Mappa")

    plt.show()
  
