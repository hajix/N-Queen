# -*- coding: utf-8 -*-

import operators
import random
import copy

class GA(object):

    @property
    def pop(self):
        return self._pop

    @property
    def eval(self):
        return self._eval

    @property
    def gen(self):
        return self._gen

    # generate initial population randomly
    def __init__(self, pop_size=100, n=8):
        self._gen = 0
        self._eval = 0
        self._pop = []
        for i in range(pop_size):
            self._pop.append(operators.generate_permutation(n))

    # select parents, mating chromosomes and insert childrens in population
    def generation(self, random_selections=5):
        self._gen += 1
        # parent selection
        candid_parents = []
        candid_fitness = []
        for i in range(random_selections):
            candid_parents.append(self._pop[random.randint(0, len(self._pop) - 1)])
            self._eval += 1
            candid_fitness.append(operators.fitness(candid_parents[i]))
        sorted_fitness = copy.deepcopy(candid_fitness)
        sorted_fitness.sort(reverse=True)
        parent1 = candid_parents[candid_fitness.index(sorted_fitness[0])]
        candid_parents.remove(parent1)
        parent2 = candid_parents[candid_fitness.index(sorted_fitness[1]) - 1]
        # mating include recombination & mutation
        child1, child2 = operators.recombination(parent1, parent2)
        child1 = operators.mutation(child1)
        child2 = operators.mutation(child2)
        # sort childs according to thier fitness. child1 is better one
        if operators.fitness(child1) > operators.fitness(child2):
            child1, child2 = child2, child1
        # survivor selection
        # substitute 2 parents have lower fitness than childrens
        child1_sub_flag = True
        child2_sub_flag = True
        for i in range(len(self._pop)):
            # fitness evaluation
            self._eval += 1
            if ((operators.fitness(self._pop[i]) > operators.fitness(child1))
            and (child1_sub_flag is True)):
                self._pop[i] = child1
                child1_sub_flag = False
            if ((operators.fitness(self._pop[i]) > operators.fitness(child2))
            and (child2_sub_flag is True)):
                self._pop[i] = child2
                child2_sub_flag = False
                break

    # check if the termination conditions occurred
    def termination_check(self, max_eval=10000):
        for i in self._pop:
            if operators.fitness(i) == 0:
                #self._eval += 1
                return [False, i]
        if(self._eval >= max_eval):
            return [False, -1]
        return [True]

    # solve N-Queen problem
    def solver(self, max_eval=10000, random_selections=5):
        while self.termination_check(max_eval)[0]:
            self.generation(random_selections)
        final_state = self.termination_check(max_eval)
        if final_state[1] == -1:
            print('problem not solved, maximum evaluation reached')
        else:
            print(('congratulation, your GA solved the problem, the solution is: ' +
            str(final_state[1])))
        print(('generation:' + str(self._gen)))
        print(('fitness evaluation:' + str(self._eval)))
