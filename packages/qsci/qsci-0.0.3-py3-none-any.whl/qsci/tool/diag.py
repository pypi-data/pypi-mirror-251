import numpy as np 

class PauliHamiltonianSolver():

    @staticmethod
    def _getPauliMatrix(n):
        if n == 0:
            return np.array([[1.0,0.0],[0.0,1.0]])
        elif n == 1:
            return np.array([[0.0,1],[1,0]])
        elif n == 2:
            return np.array([[0.0,-1j],[1j,0]])
        elif n ==3:
            return np.array([[1.0,0],[0,-1]])
        else:
            raise Exception("n must in [0,1,2,3]")

    @staticmethod
    def _directProduct(m1,m2):
        return np.kron(m1,m2) 
    
    @classmethod
    def _pauliMatrixInFullSpace(cls,P):
        r = cls._getPauliMatrix(P[0])
        for i in P[1:]:
            r = cls._directProduct( cls._getPauliMatrix(i), r )
        return r 
    
    @classmethod
    def get_HInFullSpace(cls,h):
        xi = h.get_factor()
        P = h.get_pauliOperators() 
        r = 0.0 
        for i in range(len(xi)):
            pMatrix = cls._pauliMatrixInFullSpace( P[i] )
            r = r + xi[i] * pMatrix
        r = r + h.getdH() * np.identity( 2**h.getNq() )
        return r
    
    @classmethod 
    def getEigen(cls,h):
        """return E[*],V[*,*]
        The i-th eigenvalue is E[i] with V[:,i]

        Args:
            h (_type_): _description_
        """    
        LA = np.linalg
        hMatrix = cls.get_HInFullSpace(h)
        eigenValues, eigenVectors = LA.eigh(hMatrix)
        idx = eigenValues.argsort()#[::-1]   
        eigenValues = eigenValues[idx]
        eigenVectors = eigenVectors[:,idx]
        return eigenValues.real,eigenVectors