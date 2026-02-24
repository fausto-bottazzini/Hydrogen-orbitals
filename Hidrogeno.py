import numpy as np
import matplotlib.pyplot as plt

def rad(x):
  "angulos a radianes"
  return x*np.pi/180

print("")
print("Las degeneraciones de los numeros cuaticos son")
print("para un cierto dado valor de energia n (principal) (>0)")
print("existen valores de l (azimutal)")
print("l = 0, 1, 2, ..., n-1")
print("mientras que de m (magnetico) existen")
print("m = -l, -l+1, ..., -1, 0, 1, ..., l-1, l")
print("valores")
print("")
print("Inserte los números cuánticos (n,l,m):")
n = int(input("n:") or "1")
l = int(input("l:") or "0") 
m = int(input("m:") or "0") 
print("")
print("las representaciones polares son en un corte transversal con normal en la direccion phi")
print("Inserte el ángulo azimutal (phi):")
phi = rad(float(input("phi:") or "0")) 
print("Inserte el ángulo polar (theta):")
the = rad(float(input("theta:") or "0")) 
print("")
print("para una mejor visualización divida el valor maximo de color")
print("Inserte el factor de escala:")
esc = int(input("c:") or "10") 

a = 0.529*10**(-10) #[m] radio de Bohr
E1 = -13.6 #[eV]

def E(n):
       return E1/n**2
En = E(n)

print("")
subindice_n = {0: '\u2080', 1: '\u2081', 2: '\u2082', 3: '\u2083', 4: '\u2084', 5: '\u2085', 6: '\u2086', 7: '\u2087', 8: '\u2088', 9: '\u2089'}
subindice = ''.join(subindice_n[int(digit)] for digit in str(n))
print("La energia de ligadura es:")
print(f"E{subindice} = {En} eV")
print("")

import scipy.special
from scipy.special import genlaguerre
from scipy.special import laguerre
from scipy.special import assoc_laguerre
#assoc_laguerre(x,n,k) #grado n (q) y orden k (p)
from scipy.special import lpmv
#lpmv(m,v,x) orden m (m) grado v (l) evaluado en x
import cmath

def armonicos_esfericos(theta,phi,l,m):
       uno = np.sqrt(((2*l + 1)/(4*np.pi))*((scipy.special.factorial(l-m))/(scipy.special.factorial(l+m))))
       return uno*np.exp(1j*m*phi)*lpmv(m,l,np.cos(theta))

def psi(r,theta,phi,n,l,m):
       uno = np.sqrt(((2/(n*a))**3)*((scipy.special.factorial(n-l-1))/(2*n*(scipy.special.factorial(n+l)))))
       dos = np.exp(-r/(n*a))*(2*r/(n*a))**l
       return uno*dos*(assoc_laguerre((2*r/(n*a)),(n-l-1),(2*l+1)))*armonicos_esfericos(theta,phi,l,m)

def Pdr(psi):
       return ((psi.real)**2)+((psi.imag)**2)

r = np.linspace(0,2.5*10**-9,1000)
theta = np.linspace(0,2*np.pi,360)
R, Theta = np.meshgrid(r, theta)

A = Pdr(psi(R,Theta,phi,n,l,m))
# print(A)

import matplotlib.colors as mcolors

def linea(r,t):
       return r

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location("N")
#linea de referencia
ax.plot([the] * len(r), r)

c = ax.pcolormesh(Theta, R, A, cmap='gray', shading='auto',vmin=0,vmax= np.max(A)/esc)
fig.colorbar(c, ax=ax, label="Probabilidad")
plt.title(rf"Probabilidad $|\psi_{{{n},{l},{m}}}|^2$")

plt.figure()
plt.plot(r,Pdr(psi(r,the,phi,n,l,m)),"b.-")
#graficar el radio de bohr a
# plt.axvline(a,color = "brown", linewidth = 1, linestyle = "dashed")
# y_min,_ = plt.gca().get_ylim()
# plt.text(a, y_min*2, "a", rotation=0, color="black",verticalalignment="bottom", horizontalalignment="center")
plt.ylabel(rf"Probabilidad $|\psi_{{{n},{l},{m}}}|^2$")
plt.xlabel("r [m]")
plt.title(r"Probabilidad en la dirección $\theta$ = " + str(the*180/np.pi)+"°" + r" $\phi$ = " + str(phi*180/np.pi)+"°"  )
plt.show(block=True)
