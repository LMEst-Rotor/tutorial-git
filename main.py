from os import name
import numpy as np
import plotly.graph_objects as go
from functions import solveProblem

# PROGRAM DE UMA VIGA EULER-BERNOULLI

L = 0.35 # m
h = 0.02 # m 
b = 0.06 # m
A = b*h
I = (b*(h**3))/12 # I = b*(h^3)/12

# Definição do material

E = 7e10   # N/m2
rho = 2780 # kg/m3

# Parametros da malha 
n_ef = 100
n_nos = n_ef + 1
L_ef = L / n_ef

# Parametros dinamicos
n_gdl = 2
n_DOF = n_gdl * n_nos

# Matrizes auxiliars - conectividade

mat_connect = np.zeros((n_ef,2))
for ii in range(n_ef):
    mat_connect[ii,:] = [ii,ii+1]

gdl = np.arange(0,n_DOF,1) # gdl = 0:1:n_DOF

mat_gdl = np.zeros((n_nos,n_gdl))

for ii in range(n_nos):
    mat_gdl[ii,:] = gdl[:n_gdl]
    gdl = np.delete(gdl,range(n_gdl))

MC = np.zeros((n_ef,2*n_gdl))
for ii in range(n_ef):
    MC[ii,:n_gdl] = mat_gdl[int(mat_connect[ii,0])]
    MC[ii,-n_gdl:] = mat_gdl[int(mat_connect[ii,1])]

KK = np.zeros((n_DOF,n_DOF))
MM = np.zeros((n_DOF,n_DOF))
II = np.identity(n_DOF)

K = np.array([
                [   (12*E*I)/(L_ef**3),    (6*E*I)/(L_ef**2),  -(12*E*I)/(L_ef**3),  (6*E*I)/(L_ef**2)],
                [    (6*E*I)/(L_ef**2),         (4*E*I)/L_ef,   -(6*E*I)/(L_ef**2),       (2*E*I)/L_ef],
                [  -(12*E*I)/(L_ef**3),   -(6*E*I)/(L_ef**2),   (12*E*I)/(L_ef**3), -(6*E*I)/(L_ef**2)],
                [    (6*E*I)/(L_ef**2),         (2*E*I)/L_ef,   -(6*E*I)/(L_ef**2),       (4*E*I)/L_ef],
            ]
        )

M = np.array([
                [         (13*L_ef)/35,   (11*L_ef**2)/210,          (9*L_ef)/70,    -(13*(L_ef**2))/420],
                [   (11*(L_ef**2))/210,      (L_ef**3)/105,   (13*(L_ef**2))/420,       -(L_ef**3)/140],
                [          (9*L_ef)/70, (13*(L_ef**2))/420,         (13*L_ef)/35,  -(11*(L_ef**2))/210],
                [  -(13*(L_ef**2))/420,     -(L_ef**3)/140,  -(11*(L_ef**2))/210,        (L_ef**3)/105],
        ]
    )

M *= rho*A

for ii in range(n_ef):
    aux = II[MC.astype(int)[ii,:],:]

    KK = KK + (aux.T.dot(K)).dot(aux)
    MM = MM + (aux.T.dot(M)).dot(aux)

# Aplicação das condições de contorno

noE = 0
ddlE = np.array([np.arange(0,n_gdl)],dtype=int)
posE = mat_gdl[noE,ddlE].astype(int)

MM = np.delete(MM,posE,0)
MM = np.delete(MM,posE,1)

KK = np.delete(KK,posE,0)
KK = np.delete(KK,posE,1)

# Análise dos modos

modo, Lo = solveProblem(KK,MM,L,L_ef,n_gdl)

fig = go.Figure()
qtd_modos = 5

for mode in range(qtd_modos):
    fig.add_trace(go.Scatter(x=Lo,y=modo[:,mode],name=f"{mode + 1} modo de vibrar"))

fig.show()
