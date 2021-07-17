import numpy as np

gene_set = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_ 0123456789')
target = list('Genetic Algorithm')

class Individual():
    def __init__(self):
        self.chromosome = []
        c = np.random.choice(gene_set,size=len(target))
        self.chromosome = c
        
    def fitness(self):
        fit = 0.0
        for g,t in zip(self.chromosome,target):
            if g == t :
                fit += 1
        return fit

 class GA():
    def __init__(self):
        self.population = []
        self.pop_size = pop_size
        for _ in range(pop_size) :
            ind = Individual()
            self.population.append(ind)
        self.sort()
    
    def select(self):
        p = np.random.choice(self.population)        
        return p
    
    def crossover(self,ind1,ind2):
        # select crossover point 
        l = min(len(ind1.chromosome),len(ind2.chromosome))
        cp = np.random.randint(0,l-1)        

        #swap gene
        new_chromosome = []
        new_chromosome.extend(ind1.chromosome[cp:])
        new_chromosome.extend(ind2.chromosome[:cp])
        
        offspring = Individual()
        offspring.chromosome = new_chromosome

        return offspring
    
    def mutate(self,ind):
       # indpb is chance of mutation happen
        for i in range(len(ind.chromosome)):
            if np.random.rand() <= indpb:
                mt = np.random.choice(gene_set)
                ind.chromosome[i] = mt
        return ind
    
    def sort(self):
        self.population = sorted(self.population,key=lambda x : x.fitness())
    
    def elitism(self):
        elites = []
        elite_size = round(self.pop_size * rate)
        elites.extend(self.population[-elite_size:])
        return elites
    
    def evolute(self):
        # get elite
        gt = self.elitism()
        
        while len(gt) < self.pop_size :
            # select parent
            p1 = self.select()
            p2 = self.select()
        
            # crossover to get new offspring
            offspring = self.crossover(p1,p2)
            mutated = self.mutate(offspring,indpd=0.1)
            gt.append(mutated)
            
def get_the_best(pop):
    return pop[-1]
    
def display(ind):
    return "{},{}".format (''.join(ind.chromosome),ind.fitness())
  
if __name__ == "__main__":
    pop_size = 100
    epochs = 5000
    epoch = 0
    log = []
    ga = GA(pop_size) # create population size 10
    best = get_the_best(ga.population)
    while not best.chromosome == target and epoch < epochs :
        ga.evolute()
        best = get_the_best(ga.population)
        if epoch % 50 == 0 :
            print("Epoch {} : {}".format(epoch,display(best)))
            log.append(best.fitness())
        epoch += 1
            
        # move to next generation    
        self.population = gt
        
        # sort population
        self.sort()
