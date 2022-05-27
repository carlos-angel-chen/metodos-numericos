import numpy as np
from numpy import linspace
from math import ceil
import matplotlib.pyplot as plt


#Función:   ruku4
#           Resuelve de forma aproximada el sistema de ecuaciones diferenciales:
#               dx/dt = f(t,x)  t>t0
#               x(t0)=x0
#           Emplea el método de Runge-Kutta 4
#Recibe:    f:     handle a la funcion f = dx/dt
#           t0,tf: tiempo inicial y final
#           h:     paso de integración
#           x0:    condición inicial
#Devuelve:  t:     arreglo con los instantes de tiempo
#           x:     aproximaciones numéricas a x (una fila por instante de tiempo)
def ruku4(f,t0,tf,h,x0):
    n = x0.shape[0] # número de componentes de x
    if h <= 0:      # si el paso de integración no es positivo, informa el error
        print("h debe ser mayor a 0")
        return np.zeros(1),np.zeros((n,1))
    N = int(ceil((tf-t0)/h)) # cantidad de pasos. Se toma la función techo para
    # que la h empleada sea a lo sumo tan grande como la pedida
    t = linspace(t0,tf,N+1) # arreglo de tiempos
    x = np.zeros((n,N+1))   # matriz con el resultado
    x[:,0] = x0 # los valores iniciales son dato

    for k in range(N):  # por cada paso del algoritmo...
        tk=t[k]         # se extraen los valores de x(k) y t(k)
        xk=x[:,k]

        # Y se aplica el algoritmo de Runge-Kutta 4
        f1 = f(tk, xk) 
        f2 = f(tk+h/2, xk+f1*h/2)
        f3 = f(tk+h/2, xk+f2*h/2)
        f4 = f(tk+h, xk+f3*h)
        x[:,k+1]=xk+h*(f1+2*f2+2*f3+f4)/6

    x = x.T
    return t,x


v0 = 0.48
#Función:   higginsselkov:
#           
#Recibe:    nada
#Devuelve:  nada
def higginsselkov():
    t0 = 0
    tf = 600                                              
    h = 0.01                                                
    x0 = np.array([2,3])      #s0,p0
    global v0
    v0 = vc = calcVc()

    t, result = ruku4(dx, t0, tf, h, x0)   
    result = result.T
    plot(t, result[0], result[1], "Higgins-Selkov model with v0 = vc")

    v0 = 0.48
    t, result = ruku4(dx, t0, tf, h, x0)   
    result = result.T
    plot(t, result[0], result[1], "Higgins-Selkov model with v0 < vc")

    v0 = 0.6
    t, result = ruku4(dx, t0, tf, h, x0)   
    result = result.T
    plot(t, result[0], result[1], "Higgins-Selkov model with v0 > vc")



def dx(t,x):
    return np.array([v0 - 0.23 * x[0] * (x[1]**2), 0.23 * x[0] * (x[1]**2) - 0.40 * x[1]])

def plot(t, s, p, title):
    plt.subplot(2, 1, 1)
    plt.plot(t, s)
    plt.ylabel('s')
    plt.title(title)

    plt.subplot(2, 1, 2)
    plt.plot(t, p)
    plt.xlabel('t')
    plt.ylabel('p')

    plt.show()

def isOsc(t0, tf, h, arr):
    dt = (tf-t0)/h
    eps = 0.01
    for i in range(2):
        min1 = min(arr[i][int(dt*2/3):int(dt*5/6)])
        min2 = min(arr[i][int(dt*5/6):int(dt)])
        max1 = max(arr[i][int(dt*2/3):int(dt*5/6)])
        max2 = max(arr[i][int(dt*5/6):int(dt)])
        if abs(min2 - min1) > eps or abs(max2 - max1) > eps:
            return False
    return True 


def calcVc():
    t0 = 0
    tf = 600                                               
    h = 0.01     
    x0 = np.array([2, 3])
    global v0
    v0 = vc = 0.48                     

    delta = 0.01
    for i in range(10):
        t, res = ruku4(dx, t0, tf, h, x0)  
        res = res.T                          
        if isOsc(t0, tf, h, res):                              
            v0 += delta                                                
            if v0 == vc:  
                delta /= 2                                             
                v0 -= delta 
        else:                                                                
            vc = v0
            delta /= 2                                            
            v0 -= delta 
    return vc


# from numpy import pi,cos,exp,sin
# import matplotlib.pyplot as plt

# R = 1e3	            #Valor de la resistencia	
# C = 1e-6	        #Valor de la capacidad
# w = 2.0*pi*1000     #frecuencia angular de la señal de entrada
# A = 1.0		        #amplitud de la señal de entrada
# T = 5*2*pi/w	    #simulo cinco ciclos
# def xsol(t):
#     x = -exp(-t/(R*C))+cos(w*t)+w*R*C*sin(w*t)
#     x = (A/(1+(w*R*C)**2))*x
#     return x
# def dx(t,x):
#     return ((A*cos(w*t)-x)/(R*C))

# x0 = np.zeros(1)

# t4,x4 = ruku4(dx,0,T,0.0001,x0)
# t = linspace(0,T,int(10e5))
# x = xsol(t)

# plt.plot(t,x,t4,x4)
# plt.show()
