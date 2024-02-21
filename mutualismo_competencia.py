# -*- coding: utf-8 -*-
"""Mutualismo-Competencia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19IDBYr3KOHXPphjsFC_uzCNAegSDGheq

# Importar
"""

import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from scipy.integrate import odeint

"""# Funciones de ayuda"""

# Lotka Volterra mutualismo
def sim(variables, t, params):

      # fish population level
      x = variables[0]
      # bear population level
      y = variables[1]
      r1 = params[0]
      r2 = params[1]
      alpha = params[2]
      beta = params[3]
      delta = params[4]
      gamma = params[5]

      dxdt = r1*x*(1 - alpha*x + beta* y)
      dydt = r2*y*(1 + delta*x - gamma*y)

      return([dxdt, dydt])

# Lotka Volterra competencia
def sim1(variables, t, paramsc):

    # fish population level
    x = variables[0]

    # bear population level
    y = variables[1]


    alpha = paramsc[0]
    beta = paramsc[1]
    delta = paramsc[2]
    gamma = paramsc[3]

    dxdtc = alpha * x - beta * x * y
    dydtc = delta * x * y - gamma * y

    return([dxdtc, dydtc])

"""#Trueque en el tiempo dentro de los dos grupos (mutualismo interno)"""

# Genero un vector de trueque Pi asignando a cada uno de sus 12 elementos (personas)
# una cantidad aleatoria de capacidad de trueque (bienes + servicios) por actualizar.

Pi=np.random.randint(1, 51, size=12)
Pi1=np.random.randint(1, 51, size=12)
# P es una copia de Pi que la voy a ir modificando con los trueques. P contiene la cantidad
# total de capacidad de trueque para cada tiempo
P = Pi.copy()
P1 = Pi1.copy()
inicial = np.concatenate((Pi, Pi1))
varianza0=np.var(inicial)
#M = np.concatenate((P, P1))
M = []
t = np.arange(0, 201, 1)
n=len(P)
#Esto usé para ayudarme a establecer la mínima varianza
varP = np.zeros(len(t))
varP1 = np.zeros(len(t))
# Todo este código hace las transacciones a lo largo del tiempo de manera que cada vez que una persona gana 1 bien o servicio
# otra pierde un bien o servicio
for step in range(len(t)):
    #Toma cada uno de los 4 grupos de tres personas y en cada grupo escoge una al azar que va a dar un bien o servicio (-1 bien o servicio)
  #y las otras compiten con un algoritmo basado en lotka-volterra mutualismo
  varP[step] = np.var(P)
  varP1[step] = np.var(P1)

  for _ in range(4):

    iq = random.randint(0, n-1)
    iq1 = random.randint(0, n-1)
    ilv1 = random.randint(0, n-1)
    ilv11 = random.randint(0, n-1)
    ilv2 = random.randint(0, n-1)
    ilv12 = random.randint(0, n-1)

    P[iq] -= 1
    P1[iq1] -= 1
    # Inicializar y0 con la capacidad de trueque de las personas elegidas a interactuar en mutualismo
    y0 = [Pi[ilv1],Pi[ilv2]]
    y10 = [Pi1[ilv11],Pi1[ilv12]]

    # Se avanza en el tiempo paso a paso para ser evaluado a cada instante en odeint

    tn = np.arange(0, (step+1), 1)

    params = [0.01, 0.01, 0.2, 0.1, 0.1, 0.2]

    # result contiene la derivada de la capacidad de trueque
    result = odeint(sim, y0, tn, args=(params,))
    result1 = odeint(sim, y10, tn, args=(params,))
    R=result[-1,:]
    R1=result1[-1,:]
    dxdt, dydt = sim(R,tn,params)
    dxdt1, dydt1 = sim(R1,tn,params)
    # Al comparar las derivadas se decide darle un bien o servicio al que tenga el valor mayor de derivada
    if dxdt > dydt:
      P[ilv1] += 1
    else:
      P[ilv2] += 1

    if dxdt1 > dydt1:
      P1[ilv11] += 1
    else:
      P1[ilv12] += 1
    nfil = np.concatenate((P, P1))
    M.append(nfil)
    #M=np.vstack([M, nfil])

    #print(step,P, P1)
# Aquí se identifica una fila de la matriz M de acuerto a la menor varianza encontrada ya sea en P o en P1
indopt = np.argmin(varP)
indopt1 = np.argmin(varP1)
if indopt <=  indopt1:
   m = indopt
   Fini = M[4*(m+1)]
else:
   m = indopt1
   Fini = M[4*(m+1)]
# A partir de esa fila tenemos PP y PP1
# Primero saco una copia de la última fila de este proceso para abajo hacer un gráfico de barras
fini=Fini.copy()
PP = Fini[:12]
PP1 = Fini[12:]
# Esta es la primera parte de la matriz total que va a alimentar la red neuronal
L = M[:4*(m+1)]

varianza1 = np.var(fini)

M

"""#Gráfico de la varianza vs tiempo"""

fig, axs = plt.subplots(2, 1, figsize=(5, 4), sharex=True)

# Primer gráfico
axs[0].plot(t, varP, label='Varianza P')
axs[0].set_ylabel('Varianza')
axs[0].set_title('Evolución de la Varianza')
axs[0].legend()

# Segundo gráfico
axs[1].plot(t, varP1, label='Varianza P1', color='orange')
axs[1].set_xlabel('Tiempo')
axs[1].set_ylabel('Varianza')
axs[1].legend()

# Ajustar diseño y mostrar gráficos
plt.tight_layout()
plt.show()

"""# Gráfica de barras comparando la distribución inicial con la distribución actual"""

# Obtener el rango de índices
indices = np.arange(len(P1))

# Grafico de barras para Pi
plt.subplot(2, 2, 1)
plt.bar(indices, Pi, color='green')
plt.title('Gráfico de barras para Pi')
plt.xlabel('Índice')
plt.ylabel('Valor')

# Gráfico de barras para PP
plt.subplot(2, 2, 2)
plt.bar(indices, PP, color='blue')
plt.title('Gráfico de barras para PP')
plt.xlabel('Índice')
plt.ylabel('Valor')

# Gráfico de barras para Pi1
plt.subplot(2, 2, 3)
plt.bar(indices, Pi1, color='green')
plt.title('Gráfico de barras para Pi1')
plt.xlabel('Índice')
plt.ylabel('Valor')

# Gráfico de barras para PP1
plt.subplot(2, 2, 4)
plt.bar(indices, PP1, color='blue')
plt.title('Gráfico de barras para PP1')
plt.xlabel('Índice')
plt.ylabel('Valor')

# Ajustar el diseño de los subgráficos
plt.tight_layout()

# Mostrar los gráficos
plt.show()

"""#Lotka Volterra entre grupos competencia"""

S=sum(PP)
S1=sum(PP1)

if S > S1:
  Y0 = [S/100,S1/100]
else:
  Y0 =[S1/100,S/100]

#t = np.arange(m, m+201, 1)
t=np.arange(0, 201, 1)
alpha = 1.1
beta = 0.4
delta = 0.1
gamma = 0.4

paramsc = [1.1, 0.4, 0.1, 0.4]

rresult = odeint(sim1, Y0, t, args=(paramsc,))

print(S,S1)

"""#Gráfico LV entre grupos"""

# Gráfico
plt.figure(figsize=(10, 6))

# Población de peces en el eje vertical
plt.plot(t, rresult[:, 0], label='Peces', color='blue')

# Población de osos en el eje vertical
plt.plot(t, rresult[:, 1], label='Osos', color='orange')

# Configuración del gráfico
plt.title('Dinámica de Poblaciones')
plt.xlabel('Tiempo')
plt.ylabel('Población (en cientos)')
plt.legend()
plt.grid(True)
plt.show()

"""#Loop para concretar los trueques entre el par de grupos (competencia)"""

varnfil = np.zeros(len(t))
varPP = np.zeros(len(t))
varPP1 = np.zeros(len(t))
#MM = np.concatenate((PP, PP1))
MM=[]
for i in range(len(t)):
  minPP = min(PP)
  minPP1 = min(PP1)
  varPP[i] = np.var(PP)
  varPP1[i] = np.var(PP1)
  #print(varPP[i],varPP1[i])
  iqPP = random.randint(0, len(PP)-1)
  iqPP1 = random.randint(0, len(PP1)-1)
  #Evalúo la función derivada de las poblaciones en los valores de sus respectivas poblaciones para cada valor de tiempo
  tn = np.arange(0, (i+1), 1)
  dxdtc, dydtc = sim1(rresult[i],tn,paramsc)
  if dxdtc > dydtc:
      if Y0[0] == S/100:
        for j in range(len(PP)):
           # Buscar el elemento de PP con el menor trueque
           if PP[j] == minPP:
              PP[j] += 1
              PP1[iqPP1] -= 1  # Disminuir en uno a un elemento al azar de PP1
      else:
        for j in range(len(PP1)):
           # Buscar el elemento de PP con el menor trueque
           if PP1[j] == minPP1:
              PP1[j] += 1
              PP[iqPP] -= 1
  else:
       if Y0[0] == S/100:
         for j in range(len(PP)):
           # Buscar el elemento de PP con el menor trueque
           if PP1[j] == minPP1:
              PP1[j] += 1
              PP[iqPP] -= 1  # Disminuir en uno a un elemento al azar de PP1
       else:
         for j in range(len(PP)):
         # Buscar el elemento de PP con el menor trueque
           if PP[j] == minPP:
              PP[j] += 1
              PP1[iqPP1] -= 1
  fseg = np.concatenate((PP, PP1))
  #varnfil[i]=np.var(nfil)
  #print(varnfil[i])
  MM.append(fseg)
  #MM=np.vstack([MM, nfil])
  #print(i,nfil, PP, PP1)
# Aquí limita a la matriz MM hasta la fila que tenga mayor varianza entre las dos menores varianzas.
ioptpp = np.argmin(varPP)
ioptpp1 = np.argmin(varPP1)
if ioptpp >  indopt1:
   mm = ioptpp
   LL = MM[:mm]
else:
   mm=ioptpp1
   LL = MM[:mm]
# Elimino la primera fila de LL porque se repite con la última de L
LL=LL[1:]
#  Esta sería la última fila de todo el arreglo.
ulf=LL[-1:][0]



varianza2=np.var(ulf)

"""# Graficas de las varianzas para el caso de competencia"""

fig, axs = plt.subplots(2, 1, figsize=(8, 4), sharex=True)

# Primer gráfico
axs[0].plot(t, varPP, label='Varianza PP')
axs[0].set_ylabel('Varianza')
axs[0].set_title('Evolución de la Varianza')
axs[0].legend()

# Segundo gráfico
axs[1].plot(t, varPP1, label='Varianza PP1', color='orange')
axs[1].set_xlabel('Tiempo')
axs[1].set_ylabel('Varianza')
axs[1].legend()

# Ajustar diseño y mostrar gráficos
plt.tight_layout()
plt.show()

print(varianza0, varianza1, varianza2)

"""# Grafico de barras de trueque entre grupos (competencia)"""

# Obtener el rango de índices
indices = np.arange(len(inicial))

# Grafico de la distribución de trueques inicial
plt.subplot(2, 2, 1)
plt.bar(indices, inicial, color='green')
plt.title('Trueque inicial')
plt.xlabel('Índice')
plt.ylabel('Valor')

indices1 = np.arange(len(fini))
# Distribución de trueques mutualismo
plt.subplot(2, 2, 2)
plt.bar(indices1, fini, color='blue')
plt.title('Trueque mutualismo')
plt.xlabel('Índice')
plt.ylabel('Valor')

indices1 = np.arange(len(ulf))
# Distribución de trueques final
plt.subplot(2, 2, 3)
plt.bar(indices1, ulf, color='orange')
plt.title('Trueque final')
plt.xlabel('Índice')
plt.ylabel('Valor')


# Ajustar el diseño de los subgráficos
plt.tight_layout()

# Mostrar los gráficos
plt.show()