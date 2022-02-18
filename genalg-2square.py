import random
import bitstring
import math
import numpy as np
from datetime import datetime
import concurrent.futures


class RequirementMet(Exception):
    pass

accuracy = 0.0000001
start_time = datetime.now() 
gencount = 0
inf = float("inf")
numthreads = 6
mutRate = 0.001

def eggholder(x,y):
    return (-(y+47)*math.sin(math.sqrt(abs(x/2+(y+47)))))-(x*math.sin(math.sqrt(abs(x-(y+47)))))

def firstgen(length):
    global gencount
    population = []
    gencount = 1
    for x in range(length):
        population.append(random.uniform(1,2))
    evaluate(population)
    return population

def generate(poplength=1500):
    global gencount
    try:
        pop = firstgen(poplength)
        while True:
            slicesize = len(pop)//numthreads
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for i in range(numthreads-1):
                    future = executor.submit(nextgen, pop[i*slicesize:(i+1)*slicesize])
                    futures.append(future)
                future = executor.submit(nextgen, pop[(numthreads-1)*slicesize:])
                futures.append(future)
                newpop = []
                for f in futures:
                    newpop.extend(f.result())
            pop = newpop
            gencount+=1
            evaluate(pop)
  
       
    except KeyboardInterrupt:
        end_time = datetime.now()
        file = open("population2square.txt",'w')
        file.write(str(len(pop)) + '\n')
        for p in pop:
            file.write(str(p) + '\n')
                       
        file.write('time: (hh:mm:ss.ms) {}'.format(end_time-start_time))
        file.close()
    except RequirementMet:
        end_time = datetime.now()
        file = open("population2square.txt",'w')
        file.write(str(len(pop)) + '\n')
        for p in pop:
            file.write(str(p) + '\n')
                       
        file.write('time: (hh:mm:ss.ms) {}'.format(end_time-start_time))
        file.close()
    
        



def fitness(individual):
    return abs(2-(individual*individual))

# mutacia, flipneme jeden bit v jednincovi s pravdepodobnostou mutRate
def mutate(individual, mutRate):
    retval = individual
    if random.random() < mutRate: 
        idx = random.randrange(63) # nahodne cele cislo od 0 do 127(pozicia v dvoch float cislach - obe po 64 bitov)
        retval = bitflip(individual,idx)       
    return retval


#  krizenie na nahodnej pozicii, vratime deti
def cross(parent1,parent2):
    child1, child2 = parent1,parent2
    idx = random.randrange(63)
    child1, child2 = crossone(parent1,parent2,idx)
   
    return child1,child2

def selection(population):
    newpop = []
    
    numpairings = random.randint(len(population)//2-2,(len(population)//2)+3)

    random.shuffle(population)
    for i in range(numpairings):
        start = random.randint(0, len(population)-16)
        win = tournament(population[start:start+16])
        ch1, ch2 = cross(population[i],win)
        newpop.append(ch1)
        newpop.append(ch2)
        
        
    return newpop

def tournament(subpop):
    winner = subpop[-1]
    for i in range(len(subpop)-1):
        if fitness(subpop[i])<fitness(winner):
            winner = subpop[i]
    return winner

def nextgen(population):
    global gencount
    nextpop = selection(population)
    mutedpop = nextpop
    for i in range(len(nextpop)):
        mutedpop[i] = mutate(nextpop[i],mutRate)
    gencount += 1 
    return mutedpop
        
def evaluate(population):
    fit =[fitness(p) for p in population]   
               
    mean = np.mean(fit)
    minimum = np.min(fit)
    if minimum < accuracy:
        raise RequirementMet
    
    cur_time = datetime.now()

    print('---------------------------------------------------------------------------')
    print('Generacia: ' + str(gencount))
    print('pocet jedincov: ' + str(len(population)))
    print('priemerny fitness: ' + str(mean))
    print('najmensi fitness: ' + str(minimum))
    print('cas spracovania: (hh:mm:ss.ms) {}'.format(cur_time-start_time))
    print('---------------------------------------------------------------------------')

    return mean,minimum

    

# pomocna funkcia na flipnutie jednho bitu vo float-e
def bitflip(x,pos):
    if pos < 12:
        return x # nemutovat na exponente
    bits = bitstring.BitArray(float=x,length=64)
    bits.invert(pos)
    return bits.float


# pomocna funkcia na cross v ramci jedneho floatu
def crossone(x,y,pos):
    bitsx = bitstring.BitArray(float=x,length=64)
    bitsy = bitstring.BitArray(float=y,length=64)
    tempx = bitsx[:pos]
    tempy = bitsy[:pos]
    tempx.append(bitsy[pos:])
    tempy.append(bitsx[pos:])
    return tempx.float,tempy.float

generate(5000)