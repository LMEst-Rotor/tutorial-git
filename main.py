
import numpy as np
from scipy.linalg import eigh
import plotly.graph_objects as go

# PROGRAM DE UMA VIGA EULER-BERNOULLI

class BeamEB:
    """Creates a beam element using Euler-Bernoulli theory, considering 2 degrees of freedom per node.

        Parameters
        ----------
        L : float
            Length of the beam.
        h : float
            Height of the beam
        b : float
            Width of the beam.
        E : float
            Young's modulus.
        rho : float
            Density.
        n_ef : int
            Number of finite elements.
        
        Attributes
        ----------
        matrices : tuple
            Contains the stiffness and mass global matrices, respectively.
    """ 

    def __init__(self,L,h,b,E,rho,n_ef):
        
        self.L = L
        self.h = h
        self.b = b
        self.n_ef = n_ef
        self.n_gdl = 2

        self.E = E
        self.rho = rho
        
        self.A = b*h
        self.I = (b*(h**3))/12
        self.L_ef = L / n_ef

        self.n_nos = n_ef + 1
        
        self.n_DOF = self.n_gdl * self.n_nos

        self.matrices = self.mountMatrices()

    def mountMatrices(self):
        """Mounts the Stiffness and Mass global matrices.

        Returns
        -------
        KK : numpy.ndarray
            Stiffness global matrix.
        MM : numpy.ndarray
            Mass global matrix.
        """

        mat_connect = np.zeros((self.n_ef,2))
        for ii in range(self.n_ef):
            mat_connect[ii,:] = [ii,ii+1]

        gdl = np.arange(0,self.n_DOF,1) # gdl = 0:1:n_DOF

        self.mat_gdl = np.zeros((self.n_nos,self.n_gdl))

        for ii in range(self.n_nos):
            self.mat_gdl[ii,:] = gdl[:self.n_gdl]
            gdl = np.delete(gdl,range(self.n_gdl))

        MC = np.zeros((self.n_ef,2*self.n_gdl))
        for ii in range(self.n_ef):
            MC[ii,:self.n_gdl] = self.mat_gdl[int(mat_connect[ii,0])]
            MC[ii,-self.n_gdl:] = self.mat_gdl[int(mat_connect[ii,1])]
        
        KK = np.zeros((self.n_DOF,self.n_DOF))
        MM = np.zeros((self.n_DOF,self.n_DOF))
        II = np.identity(self.n_DOF)

        K = self.K(self.E,self.L_ef,self.I)
        M = self.M(self.L_ef)

        for ii in range(self.n_ef):
            aux = II[MC.astype(int)[ii,:],:]

            KK = KK + (aux.T.dot(K)).dot(aux)
            MM = MM + (aux.T.dot(M)).dot(aux)

        return KK,MM

    def K(self,E, L_ef, I):
        """Elemental stiffness matrix

        Parameters
        ----------
        E : float
            Young's modulus.
        L_ef : float
            Length of each element.
        I : float
            Moment of inertia.

        Returns
        -------
        K : numpy.ndarray
            Stiffness elemental matrix.
        """
        K = np.array([
                [   (12*E*I)/(L_ef**3),    (6*E*I)/(L_ef**2),  -(12*E*I)/(L_ef**3),  (6*E*I)/(L_ef**2)],
                [    (6*E*I)/(L_ef**2),         (4*E*I)/L_ef,   -(6*E*I)/(L_ef**2),       (2*E*I)/L_ef],
                [  -(12*E*I)/(L_ef**3),   -(6*E*I)/(L_ef**2),   (12*E*I)/(L_ef**3), -(6*E*I)/(L_ef**2)],
                [    (6*E*I)/(L_ef**2),         (2*E*I)/L_ef,   -(6*E*I)/(L_ef**2),       (4*E*I)/L_ef],
            ]
        )
        
        return K
    
    def M(self,L_ef):
        """Elemental Mass matrix

        Parameters
        ----------
        L_ef : float
            Length of each element.

        Returns
        -------
        M : numpy.ndarray
            Mass elemental matrix.
        """    

        M = np.array([
                [         (13*L_ef)/35,   (11*L_ef**2)/210,          (9*L_ef)/70,    -(13*(L_ef**2))/420],
                [   (11*(L_ef**2))/210,      (L_ef**3)/105,   (13*(L_ef**2))/420,       -(L_ef**3)/140],
                [          (9*L_ef)/70, (13*(L_ef**2))/420,         (13*L_ef)/35,  -(11*(L_ef**2))/210],
                [  -(13*(L_ef**2))/420,     -(L_ef**3)/140,  -(11*(L_ef**2))/210,        (L_ef**3)/105],
        ]
    )

        return self.rho*self.A*M

    def runVibrationModes(self, plot=True):
        """Executes the calculus to find the vibration modes of the beam.

        Paramters
        ---------
        plot : bool, optional
            Set it False not to plot the vibration modes, and True to do it. Defaults is True.

        Returns
        -------
        modo : numpy.ndarray
            The matrix with the vibration modes of the beam. Shape is number of elements per vibration modes.
        """

        KK = self.matrices[0]
        MM = self.matrices[1]

        noE = 0
        ddlE = np.array([np.arange(0,self.n_gdl)],dtype=int)
        posE = self.mat_gdl[noE,ddlE].astype(int)

        MM = np.delete(MM,posE,0)
        MM = np.delete(MM,posE,1)

        KK = np.delete(KK,posE,0)
        KK = np.delete(KK,posE,1)

        # Análise dos modos

        modo = self.solveProblem(KK,MM)

        if plot:
            
            fig = go.Figure()
            qtd_modos = 5

            Lo = np.arange(0,self.L,self.L_ef)

            for mode in range(qtd_modos):
                fig.add_trace(go.Scatter(x=Lo,y=modo[:,mode],name=f"{mode + 1} modo de vibrar"))

            fig.show()
        
        return modo

    def solveProblem(self,KK,MM):
        """Executes the solution the eigenvalues and eigenvector's problem.

        Parameters
        ----------
        KK : numpy.ndarray
            Stiffness global matrix.
        MM : numpy.ndarray
            Mass global matrix.

        Returns
        -------
        modo : numpy.ndarray
            Eigenvectors matrix.
        """

        U, D = eigh(KK,MM)

        v = np.arange(0,len(D[:,0]),self.n_gdl)

        modo = D[v.astype(int),:]
        modo = modo/modo[-1]

        return modo
