import copy

class NO_crossover_Individual():
    def __init__(self):
        # chromosome contains 1 elements representing [r]
        self.chromosome = [np.random.rand()]
        
        
    def fitness(self):
        se = 0.0 # sum of error
        for x in lookup_table.keys():
            generated = K / (1 + b * np.exp(-self.chromosome[0] * x ))        
            observed = lookup_table[x]
            se += abs(observed - generated)
            
        # fitness is average of error    
        f = se/len(lookup_table) 
        return f
        

class NO_crossover_GA():
    def __init__(self,pop_size):
        self.population = []
        self.pop_size = pop_size
        self.k = 3
        self.elitism_rate = 0.05
        self.mutation_rate = 0.01
        
        # generate first generation
        g0 = []
        for i in range(self.pop_size):
            g0.append(NO_crossover_Individual())
        self.population = self.sort(g0)    
    
    def select(self):
        # do use tournament selection
        good_idx = round(self.pop_size*0.5)
        s1 = np.random.choice(self.population[:good_idx],size=self.k,replace=False)
        best = None
        for s in s1:
            if best is None or s.fitness() > best.fitness():
                best = s
        return best    
    
    def mutate(self,ind):
        # do a little bit change in value of each gene
        c1 = copy.deepcopy(ind)
        c2 = copy.deepcopy(ind)
        
        c1.chromosome[0] = np.random.uniform(c1.chromosome[0]-self.mutation_rate ,c1.chromosome[0])
        c2.chromosome[0] = np.random.uniform(c2.chromosome[0] ,c2.chromosome[0] + self.mutation_rate)
        
        if c1.fitness() < ind.fitness():
            ind = c1
        elif c2.fitness() < ind.fitness():
            ind = c2        
        
        return ind
    
    def sort(self,population):
        return sorted(population,key=lambda x:x.fitness())
    
    def elitism(self):
        elite=[]
        elite_size = round(self.pop_size * self.elitism_rate)
        
        # pick up the best
        elite.extend(self.population[:elite_size])
        
        return elite
    
    
        
    def evolute(self):
        # get elite from ancester
        gt = self.elitism()        
        while len(gt) < self.pop_size :
            offspring = self.select()
            offspring = self.mutate(offspring)
            
            # put new one onto the population
            gt.append(offspring)
        
        #move to next generation
        self.population = self.sort(gt)
        
        
    def get_the_best(self):
        # the best is the one with lowest fitness
        return self.population[0]       
  
  
ns_ga = NO_crossover_GA(10)
ns_ga.elitism_rate = 0.1
ns_ga.mutation_rate = 0.05
epochs = 100
epoch = 0
ns_log = []
ns_best = ns_ga.get_the_best()
print("Epoch : {}, best fitness : {}".format(epoch,ns_best.fitness()))     
while epoch < epochs and round(ns_best.fitness()) > 50 :
    ns_ga.evolute()
    ns_best = ns_ga.get_the_best()
    epoch += 1
    if epoch % 10 == 0 :
        fn = ns_best.fitness()
        ns_log.append(fn)
        print("Epoch : {}, best fitness : {}".format(epoch,fn))
print("Epoch : {}, best fitness : {}".format(epoch,ns_best.fitness()))     
