h =6.62607015*10**(-34)
e = 2.71828
k = 1.380649*10**(-23)
g=9.8
stefbol=5.670367*10**(-8)



#time
day2sec       = 86400.0 # seconds in a day  =  24h  =  86400 s
day2min       = 1440.0  # min in a day  =  1440. min
day2hour      = 24.0 # hours in a day ...
sec2day       = 1.0/day2sec
min2day       = 1.0/day2min
hour2day      = 1.0/day2hour
# body constants
GMsun_tcb = 1.32712442099e20 # Solar mass parameter: m^3/s^2 (TCB)          | +/- 1D10    |
GMsun_tdb = 1.32712440041e20 # Solar mass parameter: m^3/s^2 (TDB)          | +/- 1D10    |
#a planet
amer = 0.38709830982 
aven = 0.72332981996
aear = 1.00000101778
amars = 1.52367934191
ajup = 5.20260319132
asat = 9.55490959574
aura = 19.21844606178
anep = 30.11038686942
# masses conversions
Msmer = 6.0236e6 # Msun to Mmer
Mmers = 1.0/Msmer # Mmer to Msun
Msven = 4.08523719e5 # Msun to Mven
Mvens = 1.0/Msven   #  Mven to Msun
Msear = 332946.0487 # Msun to Mear
Mears = 1.0/Msear  #  Mear to Msun
Msmar = 3.09870359e6 # Msun to Mmar
Mmars = 1.0/Msmar   #  Mmar to Msun
Msjup = 1.047348644e3 # Msun to Mjup
Mjups = 1.0/Msjup    #  Mjup to Msun
Mssat = 3.4979018e3 # Msun to Msat
Msats = 1.0/Mssat  #  Msat to Msun
Msura = 2.290298e4 # Msun to Mura
Muras = 1.0/Msura #  Mura to Msun
Msnep = 1.941226e4 # Msun to Mnep
Mneps = 1.0/Msnep #  Mnep to Msun
# masses of Solar System objects
Msun = 1.9884e30 # Sun mass in kg
Mmer = Msun*Mmers #  Mercury mass in kg
Mven = Msun*Mvens #  Venus mass in kg
Mear = 5.9722e24 # Earth mass in kg
Mmar = Msun*Mmars #  Mars mass in kg
Mjup = Msun*Mjups #  Jupiter mass in kg
Msat = Msun*Msats #  Saturn mass in kg
Mura = Msun*Muras #  Uranus mass in kg
Mnep = Msun*Mneps #  Neptune mass in kg
# radii of Solar System objects
Rsun = 696000.0 #  Sun radius in km
Rmer = 2439.7  #  Mercury radius in km
Rven = 6051.8  #  Venus radius in km
Rear = 6378.1366 # Earth radius in km
Rmar = 3396.19 #  Mars radius in km
Rjup = 71492.0  #  Jupiter radius in km
Rsat = 60268.0  #  Saturn radius in km
Rura = 25559.0  #  Uranus radius in km
Rnep = 24764.0  #  Neptune radius in km
Rplu = 1195.0  #  Pluto radius in km
#
Rsjup = Rsun/Rjup #  Rsun to Rjup
Rjups = Rjup/Rsun #  Rjup to Rsun
#
Rejup = Rear/Rjup # Rearth to Rjupiter
Rjear = Rjup/Rear # Rjupiter to Rearth
#
Rsear = Rsun/Rear #  Rsun to Rjup
Rears = Rear/Rsun #  Rear to Rsun


# astronomical constants
AU       = 149597870700.0 #Astronomical Unit in meters
kappa    = 0.01720209895 # Gaussian gravitational constant
Giau     = kappa*kappa # G [AU^3/Msun/d^2]
G      = 6.67428e-11 #Gravitational Constants in SI system [m^3/kg/s^2]
Gaumjd   = G*day2sec*day2sec*Mjup/(AU**3) # G in [AU,Mjup,day]

c    = 299792458.0 # speed of light (c) in [m/s]
speedaud = c*day2sec/AU # speed of light in [AU/d]
pc2AU    = 206264.806 # parsec to au

# others
RsunAU = (Rsun*1.0e3)/AU #Sun radius in AU
RjupAU = (Rjup*1.0e3)/AU #Jupiter radius in AU

MJD = 2400000.5 # MJD ref time to convert to JD

sigma_sb = 5.670367e-8 # Stefan-Boltzmann constant in W⋅m^−2⋅K^−4

Teff_sun = 5772.0 # Effective Temperature of the Sun in K