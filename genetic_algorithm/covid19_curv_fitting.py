import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# parameters
K = 3062
P0 = 6
b = (K-P0)/P0

# -- create lookup table
data = pd.read_csv('covid_thailand.csv')
lookup_table = {}
for i, row in data.iterrows():
    lookup_table[row['t']]=row['cases']
    
# -- Individual 
class Individual():
    def __init__(self):
        # chromosome contains 2 elements represent [x,y]
        self.chromosome = [np.random.rand() ,np.random.normal()]
        
        
    def fitness(self):
        se = 0.0 # sum of error
        for x in lookup_table.keys():
            generated = K / (1 + b * np.exp(-self.chromosome[0] * x + self.chromosome[1]))        
            observed = lookup_table[x]
            se += abs(observed - generated)
            
        # fitness is average of error    
        f = se/len(lookup_table) 
        return f
      
      
# -- GA 
class GA():
    def __init__(self,pop_size):
        self.population = []
        self.pop_size = pop_size
        self.k = 3
        self.elitism_rate = 0.05
        self.mutation_rate = 0.01
        
        # generate first generation
        g0 = []
        for i in range(self.pop_size):
            g0.append(Individual())
        self.population = self.sort(g0)
        
    def select(self):
        # do use tournament selection
        s1 = np.random.choice(self.population,size=self.k,replace=False)
        best = None
        for s in s1:
            if best is None or s.fitness() > best.fitness():
                best = s
        return best
    
    def crossover(self,ind1,ind2):
        new_chrom = []
       
        #play coin tossing 
        p = np.random.rand()
        if p < 0.5 :
            new_chrom.append(ind1.chromosome[0])
            new_chrom.append(ind2.chromosome[1])
        else:
            new_chrom.append(ind2.chromosome[0])
            new_chrom.append(ind1.chromosome[1])

            
        offspring = Individual()
        offspring.chromosome = new_chrom
        return offspring
    
    def mutate(self,ind):
        # do a little bit change in value of each gene
        new_chrom = []
        b = ind.chromosome[0]
        r = ind.chromosome[1]
        
        b_lowest = b - self.mutation_rate
        b_highest = b + self.mutation_rate
        
        # new b must be range between b_lowest and b_highest
        b = np.random.uniform(b_lowest,b_highest)
        
        r_lowest = r - self.mutation_rate
        r_highest = r + self.mutation_rate
        
        # new r must be range between r_lowest and r_highest
        r = np.random.uniform(r_lowest,r_highest)
                
        ind.chromosome[0] = b
        ind.chromosome[1] = r
        
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
            # get parent
            p1 = self.select()
            p2 = self.select()
            
            # crossover and mutation
            offspring = self.crossover(p1,p2)
            offspring = self.mutate(offspring)
            
            # put new one onto the population
            gt.append(offspring)
        
        #move to next generation
        self.population = self.sort(gt)
        
        
    def get_the_best(self):
        # the best is the one with lowest fitness
        return self.population[0]  
      
# -- Test
ga = GA(100)
ga.elitism_rate = 0.2
ga.mutation_rate = 0.05
epochs = 1000
epoch = 0
log = []
best = ga.get_the_best()
while epoch < epochs and best.fitness() > 10:
    ga.evolute()
    best = ga.get_the_best()
    epoch += 1
    if epoch % 50 == 0 :
        fn = ga.get_the_best().fitness()
        log.append(fn)
        print("Epoch : {}, best fitness : {}".format(epoch,fn))
print("Epoch : {}, best fitness : {}".format(epoch,fn))       


# -- plot 

t =[]
pt =[]
best = ga.get_the_best()
print(best.chromosome)
for x in lookup_table.keys():
    t.append(x)
    pt.append(K/(1 + b * np.exp(-best.chromosome[0] * x + best.chromosome[1]) ))

t1=[]
pt1=[]
for k,v in lookup_table.items():
    t1.append(k)
    pt1.append(v)
    
plt.figure(figsize=(24,8))
plt.plot(t,pt,label="Estimated")
plt.plot(t1,gaussian_filter1d(pt1,sigma=1.5),label="Observed")
plt.grid(True)
plt.legend()
plt.show()
