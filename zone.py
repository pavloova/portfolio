import math as m
import matplotlib.pyplot as plt
import numpy as np
from physicalconstants import stefbol
from solar import a,e

def zones(star_rad=13920000000 ,star_temp=5772,r_edge=4504300000000 ):
    fi = np.linspace(0, 2*np.pi, 1000)
    star_lumin = 4 * m.pi * star_rad**2 * stefbol * star_temp**4
    S_inner = 4.19 * 10**(-8) * star_temp**2 - 2.319 * 10**(-4) + 1.268
    rinner = m.sqrt(star_lumin/S_inner)
    S_outer = 6.19 * 10**(-9) * star_temp**2 - 1.319 * 10**(-5) + 0.234
    router = m.sqrt(star_lumin/S_outer)
    r=star_rad*1000
    
    x =  r* np.cos(fi) 
    y = r* np.sin(fi)
    x1 = rinner * np.cos(fi)
    y1 = rinner * np.sin(fi)
    x2 = router * np.cos(fi)
    y2 = router * np.sin(fi)
    x3 = r_edge * np.cos(fi)
    y3 = r_edge * np.sin(fi)
    
    plt.rcParams['figure.facecolor']='grey'
    #plt.plot(x2, y2, color = 'b',lw=50)
    plt.grid()
    plt.fill_between(x3, y3, color = 'b')
    plt.fill_between(x2, y2, color = 'g')
    plt.fill_between(x1, y1, color = 'r')
    plt.fill_between(x, y, color = 'black')
    plt.axis('equal')

   

def orbits(a, e):
    for i in range(0,len(a), 1):
      fi = np.linspace(0, 2*np.pi, 100)
      c=np.sqrt(a[i]**2-(a[i]*np.sqrt(1-e[i]**2))**2)
      x=a[i]*np.sin(fi)+c
      y=(a[i]*np.sqrt(1-e[i]**2))*np.cos(fi)
      plt.axis('equal')
      plt.plot(x,y,color='black',lw=2)
zones()
orbits(a,e)
plt.show()
    
