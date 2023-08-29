mport matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots()
smth, = plt.plot([],[],'pink',label='Patrik Star',ms=10)

def something(ph):
    t=np.arange(0,4*np.pi,1)
    x=12*np.cos(t)+8*np.cos(1.5*t)
    y=12*np.sin(t)-8*np.sin(1.5*t)
    X= x*np.cos(ph)-y*np.sin(ph)
    Y=y*np.cos(ph)+x*np.sin(ph)
    return X,Y
def animate(i):
    smth.set_data(something(ph=i)) 
ax.set_xlim(-25,25)
ax.set_ylim(-25,25)
plt.axis('equal')
plt.grid()
plt.legend()
ani= FuncAnimation(fig,animate,interval=50,frames=100)
ani.save('aaaa.gif')
