import math
import random
import math


def eggholder(x,y):
    return (-(y+47)*math.sin(math.sqrt(abs(x/2+(y+47)))))-(x*math.sin(math.sqrt(abs(x-(y+47)))))
# energia je nulova ak som v minime
def energy(x,y):
    return eggholder(x,y) + 959.6406627106155
# metropolisov monte carlo algoritums
def metropolis(xinit,kmax,T):
    k=0
    x=xinit
    while k<kmax:
        k += 1
        xnew = Opertur(x)
        pr = min(1,math.exp((-1*(energy(xnew[0],xnew[1]))-energy(x[0],x[1]))/T))
        if random.random()< pr: 
            x=xnew
    return x
# simulovane zihanie pomocou metropolisovho alg.
def simzih(Tmin,Tmax,kmax,alpha):
    T = Tmax
    xinit = [random.uniform(-512,512),random.uniform(-512,512)]
    print('pociatocna hodnota:',xinit)
    print('energia v danom bode:',energy(xinit[0],xinit[1]))
    while T>Tmin:
        xinit = metropolis(xinit,kmax,T)
        print('zmena metropolisovym algoritmom, nova hodnota:',xinit)
        print('energia v danom bode:',energy(xinit[0],xinit[1]))
        T = alpha*T
    return xinit
# Opertur operator ?
def Opertur(x):
    y = [random.uniform(-512,512),random.uniform(-512,512)]
    return y

# spustenie skriptu
result = simzih(0.000001,100,20,0.9)
print('---------------------------------------------')
print('najdene minimum', result)
print('hodnota:',eggholder(result[0],result[1]))