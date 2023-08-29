import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots(figsize=(10,5))
lilcircle, = plt.plot([],[],'g')
point,=plt.plot([],[],'ro')
astroid, = plt.plot([],[],color='b')
R=1
def circle(R,ph):
    phi =np.linspace(0,4*np.pi,100)
    x0=R*np.cos(ph)
    y0=R*np.sin(ph)  
    x =x0+ R/4*np.cos(phi)
    y= y0+ R/4*np.sin(phi)
    return x,y

th=np.linspace(0,4*np.pi,100)
x_cycl=R*(np.sin(th))**3
y_cycl=R*(np.cos(th))**3
def animate(i):
    astroid.set_data(x_cycl[:i+1],y_cycl[:i+1])
    point.set_data(x_cycl[i],y_cycl[i])
    lilcircle.set_data(circle(R=1,ph=-i+1.55))
def just_circle(R):
    phi =np.linspace(0,4*np.pi,100)
    x=R*np.cos(phi)
    y=R*np.sin(phi)
    return(x,y)    
sub=just_circle(R=1)
plt.plot(sub[0],sub[1])
N = 100
ax.set_xlim(0,10)
ax.set_ylim(0,5)
plt.legend()
plt.axis('equal')
plt.grid()


ani= FuncAnimation(fig,animate,interval=50,frames=100)
ani.save('lilcircle.gif')

