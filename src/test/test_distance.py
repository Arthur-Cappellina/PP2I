import matplotlib.pyplot as plt 
import modules.bdd as bdd
import time
import random


LesTemps=[]
I=[(random.random()-0.5)*360 for i in range(1000)]
J=[(random.random()-0.5)*360 for i in range(1000)]
K=[(random.random()-0.5)*360 for i in range(1000)]
L=[(random.random()-0.5)*360 for i in range(1000)]
for i in range(1000):
    tps1 = time.perf_counter()
    bdd.distance(I[i],J[i],K[i],L[i])
    tps2 = time.perf_counter()
    LesTemps.append((tps2 - tps1)*1000)
NumeroTest=[i for i in range(len(LesTemps))]
plt.plot(NumeroTest,LesTemps)
plt.title('temps execution fonction distance')
plt.xlabel('Numéro du test')
plt.ylabel('Temps (ms)')
plt.show()
