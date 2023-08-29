import matplotlib.pyplot as plt
import numpy as np
from physicalconstants import stefbol
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots()
inner_boundary, = plt.plot([],[],'r-',label='habitable zone',ms=3)
outer_boundary, = plt.plot([],[],'b-',label='habitable zone',ms=3)

def zone_in(n):
    Teff=np.linspace(2660,30000,10000)
    #Rstar=np.arange(0.13*Rsun,7.4*Rsun,1.4*10**8)
    Rstar=np.linspace(90480000,5150400000,10000)
    Lstar=4*np.pi*Rstar**2*Teff**4*stefbol
    #Lstar=np.linspace(0.0008*Lsun,20000*Lsun,100000)
    #Sinner=4.19*10**(-8)*Teff**2-2.139*10**(-4)*Teff+1.268
    rinner=np.sqrt(Lstar/(4.19*10**(-8)*Teff**2-2.139*10**(-4)*Teff+1.268))*n
    t=np.linspace(0,2*np.pi,10000)
    x1= rinner*np.cos(t)
    y1=rinner*np.sin(t)
    return x1,y1
def zone_out(n):
    Teff=np.linspace(2660,30000,10000)
    Rstar=np.linspace(90480000,5150400000,10000)
    Lstar=4*np.pi*Rstar**2*Teff**4*stefbol
    Sout=6.19*10**(-9)*Teff**2-1.319*10**(-5)*Teff+0.234
    rout=np.sqrt(Lstar/Sout)*n
    t=np.linspace(0,2*np.pi,10000)
    x=rout*np.cos(t)
    y=rout*np.sin(t)
    return x,y

def animate(i):
    inner_boundary.set_data(zone_in(i))
    outer_boundary.set_data(zone_out(i))
    ax.set_xlim(-60000000000000000, 60000000000000000)
    ax.set_ylim(-60000000000000000, 60000000000000000)
    ax.axis('equal')
    return inner_boundary,outer_boundary,
ani= FuncAnimation(fig,animate,interval=100,frames=80)
ani.save('planet.gif')

