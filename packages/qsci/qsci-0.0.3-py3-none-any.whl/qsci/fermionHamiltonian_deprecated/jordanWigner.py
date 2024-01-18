import logging
import numpy as np


class PauliHamiltonian:
    """
    direct for isQ 
    """    

    def __init__(self, nq):
        self.nq = nq
        self.xi = []
        self.P = []
        self.dH = 0  # constant energy

    def copy(self):
        new = PauliHamiltonian(self.nq) 
        new.xi = list(self.xi)
        new.P = list(self.P) 
        new.dH = self.dH
        return new 

    def setOneTerm(self, xi, p):
        self.xi.append(xi)
        self.P.append(p)
        return self

    def setOneTerm_byXYZ(self, xi, X=[], Y=[], Z=[]):
        # X = [] contains all site which are acted by X ,
        p = [0] * self.nq
        for i in range(self.nq):
            if i in X:
                p[i] = 1
            elif i in Y:
                p[i] = 2
            elif i in Z:
                p[i] = 3
        self.xi.append(xi)
        self.P.append(p)

    def add_dH(self, dH):
        self.dH += dH
        return self

    def getQn(self):
        logging.warning("deprecated method, use getNq instead")
        return self.nq
    
    def getNq(self):
        return self.nq 

    def get_factor(self):
        return self.xi

    def get_pauliOperators(self):
        return self.P

    def simplify(self):
        table = {}
        for i in range(len(self.P)):
            key = str(self.P[i])
            if key not in table:
                table[key] = {
                    "xi": self.xi[i],
                    "op": list(self.P[i]),
                }
            else:
                table[key]["xi"] += self.xi[i]
        self.xi, self.P = [], []
        for k in table:
            xi = table[k]["xi"]
            if xi != 0:
                self.P.append(table[k]["op"])
                self.xi.append(table[k]["xi"])
        return self 

    def __hash__(self) -> int:
        return hash(str(hash(tuple(self.xi))) + str(hash(str(self.P))) + str(id(self)))
    
    def __len__(self):
        return len(self.P)
    
    def getdH(self):
        return self.dH
    
    def __add__(self,other):
        new = self.copy()
        if type(other) in [self.__class__]:
            for j in range(len(other.xi)):
                new.xi.append( other.xi[j] )
                new.P.append( other.P[j] )
            new.dH += other.dH 
        else:
            try:
                new.dH += float(other)
            except:
                raise Exception(f"unsupported adding with {type(other)}")
        return new 
    
    def __mul__(self,other):
        try:
            f = float(other)
            new = self.copy()
            new.xi = [ x*f for x in new.xi]
            new.dH *= f 
            return new 
        except:
            raise Exception(f"unsupported multiplexing with {type(other)}")
        
    def __repr__(self):
        def print_p(n):
            return ['I','X','Y','Z'][n]
        def print_P(P):
            return "".join([ print_p(i) for i in P])
        def print_one_line(i):
            return f"             {print_P(self.P[i])}: {self.xi[i]}"
        lines = "\n".join([ print_one_line(i)  for i in range(len(self.xi)) ])
        return f'''
        Pauli operators:
{lines}
        '''



class Hamiltonian:
    # Jordan-Wigner encoding for Fermion system

    def __init__(self, nSite: int):
        self.ns = nSite
        self.pH = PauliHamiltonian(nq=nSite)

    def set_Hopping(self, i, j, tij):
        # set  t_{ij} c^+_i c_j + t_ij^* c^+_i c_j
        tij *= 1.0
        if i > j:
            i, j = j, i
            tij = np.conjugate(tij)
        chi_ij = -np.imag(tij) * ((-1) ** (j - i)) / 2
        xi_ij = np.real(tij) * ((-1) ** (j - i)) / 2
        self.pH.setOneTerm_byXYZ(
            xi=-xi_ij, X=[], Y=[i, j], Z=[a for a in range(i + 1, j)]
        )
        self.pH.setOneTerm_byXYZ(
            xi=-xi_ij, X=[i, j], Y=[], Z=[a for a in range(i + 1, j)]
        )
        if chi_ij > 0:
            self.pH.setOneTerm_byXYZ(
                xi=-chi_ij, X=[j], Y=[i], Z=[a for a in range(i + 1, j)]
            )
            self.pH.setOneTerm_byXYZ(
                xi=chi_ij, X=[i], Y=[j], Z=[a for a in range(i + 1, j)]
            )

    def _set_DoubleTerm_Gamma(self, u, S, i, j, k, l):
        R = u.real
        I = u.imag
        kxi = (-1) ** (i + j + k + l) / 8.0
        N = [[R, I, I, R], [I, R, R, I], [I, R, R, I], [R, I, I, R]]
        # template = (
        #     [0] * i
        #     + [0]
        #     + [3] * (j - i)
        #     + [0] * (k - j)
        #     + [3] * (l - k)
        #     + [0] * (self.pH.nq - l)
        # )
        template = (
            [0] * i
            + [3] * (j - i)
            + [0] * (k - j)
            + [3] * (l - k)
            + [0] * (self.pH.nq - l - 1)
        )
        for A in range(2):
            for B in range(2):
                for C in range(2):
                    for D in range(2):
                        p = list(template)
                        p[i], p[j], p[k], p[l] = A + 1, B + 1, C + 1, D + 1
                        x, y = A * 2 + B, C * 2 + D
                        xi = kxi * N[x][y] * S[x][y]
                        self.pH.setOneTerm(xi=xi, p=p)
        return self

    def _set_DoubleTerm_ijkl_type1(self, i, j, k, l, u):
        # see details in notebook
        # u c^+_i c^+_j c_k c_l
        S = [[-1, -1, -1, 1], [1, -1, -1, -1], [1, -1, -1, -1], [1, 1, 1, -1]]
        return self._set_DoubleTerm_Gamma(u, S, i, j, k, l)

    def _set_DoubleTerm_ijkl_type2(self, i, j, k, l, u):
        # see details in notebook
        # u c^+_i c_j c^+_k c_l
        S = [[1, 1, -1, 1], [1, -1, 1, 1], [-1, 1, -1, -1], [1, 1, -1, 1]]
        return self._set_DoubleTerm_Gamma(u, S, i, j, k, l)

    def _set_DoubleTerm_ijkl_type3(self, i, j, k, l, u):
        # see details in notebook
        # u c^+_i c_j c_k c^+_l
        S = [[-1, 1, -1, -1], [-1, -1, 1, -1], [1, 1, -1, 1], [-1, 1, -1, -1]]
        return self._set_DoubleTerm_Gamma(u, S, i, j, k, l)

    def set_cdcdcc(self, i, j, k, l, u):
        """
        U_{i,j,k,l} c^+_i c^+_j c_k c_l + h.c.
        """
        assert i != j != k != l

        if min(i, j, k, l) in [k, l]:
            return self.set_cdcdcc(l, k, j, i, u=u.conjugate())
        # --- now min must in [i,j]
        if i > j:
            return self.set_cdcdcc(j, i, k, l, u=-u)
        # --- now min=i
        if j < k < l:
            return self._set_DoubleTerm_ijkl_type1(i, j, k, l, u)
        if j < l < k:
            return self._set_DoubleTerm_ijkl_type1(i, j, l, k, -u)
        if k < j < l:
            return self._set_DoubleTerm_ijkl_type2(i, k, j, l, -u)
        if k < l < j:
            return self._set_DoubleTerm_ijkl_type3(i, k, l, j, u)
        if l < j < k:
            return self._set_DoubleTerm_ijkl_type2(i, l, j, k, u)
        if l < k < j:
            return self._set_DoubleTerm_ijkl_type3(i, l, k, j, -u)

    def set_Onsite(self, i, m):
        self.pH.setOneTerm_byXYZ(xi=m / 2, Z=[i])
        self.pH.add_dH(m / 2)

    def set_Hx(self,i,m):
        # this potential seems not well defined
        '''similar to set_Onsite, but on x direction'''
        self.pH.setOneTerm_byXYZ(xi=m / 2, X=[i])
        self.pH.add_dH(m / 2)

    def set_Coulomb(self, i, j, U):
        # for spinless system, i!=j
        if i == j:
            logging.error("in spinless system i!=j !!!")
        self.pH.setOneTerm_byXYZ(xi=U / 4, Z=[i])
        self.pH.setOneTerm_byXYZ(xi=U / 4, Z=[j])
        self.pH.setOneTerm_byXYZ(xi=U / 4, Z=[i, j])
        self.pH.add_dH(U / 4)

    def getPauliHam(self):
        self.pH.simplify()
        return self.pH

    def generateC(self, i):
        nq = self.pH.getQn()
        xi = [((-1) ** i) / 2, ((-1) ** i) / 2 * (-1j)]
        P1 = [3] * (i) + [1] + [0] * (nq - i - 1)
        P2 = [3] * (i) + [2] + [0] * (nq - i - 1)
        return xi, [P1, P2]

    def generateCdagger(self, i):
        xi, P = self.generateC(i)
        xid = [np.conjugate(xi[0]), np.conjugate(xi[1])]
        return xid, P

    def test(self):
        return JordanWigner_FermionHamiltonian


class SpinfullHamiltonian:
    # pair encoding, that is siteI = (2*i,2*i+1)

    def __init__(
        self,
        nSite: int,
    ):
        self.ns = nSite
        self.h = Hamiltonian(nSite * 2)

    def set_spinHopping(self, i, j, spin, tij):
        self.h.set_Hopping(i=2 * i + spin, j=2 * j + spin, tij=tij)
        return self 

    def set_Hopping(self, i, j, tij):
        self.set_spinHopping(i=i, j=j, spin=0, tij=tij)
        self.set_spinHopping(i=i, j=j, spin=1, tij=tij)
        return self 

    def set_chemicalPotential(self, i, mu):
        self.h.set_Onsite(i * 2, -mu)
        self.h.set_Onsite(i * 2 + 1, -mu)
        return self 

    def set_onSiteCoulombU(self, i, U):
        self.h.set_Coulomb(i=2 * i, j=2 * i + 1, U=U)
        return self 
    
    def set_globalCoulombU(self,U):
        for i in range(self.ns):
            self.set_onSiteCoulombU(i,U) 
        return self
    
    def set_globalOnSiteEnergy(self,m):
        for i in range(self.ns):
            self.set_chemicalPotential(i, -m)
        return self


    def getPauliHam(self):
        return self.h.getPauliHam()
    
    def getHam(self):
        """get Fermion Hamiltonian
        """        
        return self.h 


# class Hubbard():

#     def __init__(self,int: nSite, qubitMap=None):
#         self.ns = nSite


# https://math.berkeley.edu/~linlin/2018Spring_290/SRL12.pdf Bravyi-Kitaev transformation
