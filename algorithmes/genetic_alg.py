import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import pygad


class GeneticAlg:
    @classmethod
    def genetic_alg(cls, iteration_num, parent_num, fitness,
                    number_of_solutions, num_genes, crossover_probability,
                    mutation_probability, after_mutation_func):
        # initial_population is built by sol_per_pop and num_genes
        # num_genes = Number of genes in the solution / chromosome
        ga_instance = pygad.GA(num_generations=iteration_num,
                               num_parents_mating=parent_num,
                               fitness_func=fitness,
                               sol_per_pop=number_of_solutions,
                               num_genes=num_genes,
                               gene_type=float,
                               init_range_low=0.0,
                               init_range_high=1.0,
                               parent_selection_type="rws",
                               keep_parents=0,
                               crossover_type="single_point",
                               crossover_probability=crossover_probability,
                               mutation_type="random",
                               mutation_probability=mutation_probability,
                               mutation_by_replacement=False,
                               random_mutation_min_val=0.0,
                               random_mutation_max_val=1.0,
                               on_mutation=after_mutation_func)
        ga_instance.run()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        print("Parameters of the best solution : {solution}".format(solution=solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
        filename = 'genetic'
        ga_instance.save(filename=filename)
        loaded_ga_instance = pygad.load(filename=filename)
        return loaded_ga_instance.best_solution()

    @classmethod
    def on_mutation(cls, ga_instance, offspring_mutation):
        for chromosome in offspring_mutation:
            sum_ = 0
            for q in chromosome:
                if q < 0:
                    offspring_mutation.remove(chromosome)
                    break
                sum_ += q
            if sum_ > 1:
                offspring_mutation.remove(chromosome)
        return offspring_mutation
