import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from math import sqrt
fig, ax = plt.subplots()
smth, = plt.plot([],[],'r-o',label='square',ms=5)

def something(a,ph):
    #t=np.linspace(0,4*np.pi,6) при 6 шагах получается красивая звездочка
    t=np.linspace(0,4*np.pi,9)
    
    d=a*sqrt(2)/2
    x=d*np.cos(t)
    y=d*np.sin(t)
    X= x*np.cos(ph)-y*np.sin(ph)
    Y=y*np.cos(ph)+x*np.sin(ph)
    return X,Y
def animate(i):
    smth.set_data(something(a=1,ph=i)) 
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
plt.axis('equal')
plt.grid()
plt.legend()
ani= FuncAnimation(fig,animate,interval=100,frames=80)
ani.save('square.gif')

"""прикольная крутящаяся штука
def something(a,ph,m):

    t=np.linspace(0,4*np.pi,m)
    d=a*sqrt(2)/2
    x=d*np.cos(t)
    y=d*np.sin(t)
    X= x*np.cos(ph)-y*np.sin(ph)
    Y=y*np.cos(ph)+x*np.sin(ph)
    return X,Y    
    
def animate(i):
    smth.set_data(something(a=1,ph=i,m=i)) 
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
plt.axis('equal')
plt.grid()
plt.legend()
ani= FuncAnimation(fig,animate,interval=100,frames=80)
ani.save('aaaa.gif')"""
