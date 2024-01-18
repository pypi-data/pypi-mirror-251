from __future__ import annotations
import logging
from ...utils import VariableTypeChecker
# from lattpy import Lattice,SiteOccupiedError
from .fermion import SpinlessHamiltonian
from ...utils import CacheDict as CacheDict
import numbers
import numpy as np 
import math 
import random
import string
import typing

Vector = typing.Any

class FermionLatticeError(Exception):pass 



# class _Orbit():

#     def __init__(self,pos,name):
#         self.pos = np.array(pos) # real pos as one want  
#         self.name = name 
#         self.latticePos = self.pos 
#         self._delta = self.pos - self.latticePos

#     def _epsilonV(self):
#         d = len(self.pos)
#         return np.array([1e-7]*d)
    
#     def getPos(self):
#         """the real position we want
#         """        
#         return self.pos 
        
#     def attach2Lattice(self,lattice):
#         iMax = 20
#         i = 0
#         while True:
#             try:
#                 lattice.add_atom(pos= self.latticePos , atom=self.name) 
#                 return self 
#             except SiteOccupiedError:
#                 i += 1 
#                 self.latticePos = i * self._epsilonV() + self.pos 
#                 self._delta = self.pos - self.latticePos
#                 if i == iMax:
#                     raise FermionLatticeError(f"more than {iMax} orbits in one position?")
#             except:
#                 raise 





# class LatticeStructure():
#     """define the Hamiltonian of a lattice 
#     """    
#     def __init__(self,basis):
#         self.lattice = Lattice(basis)
#         self._orbits = {} 
#         self._interaction = {} 

#     # def _getRandomOrbitName(self):
#     #     while True:
#     #         s = ''.join(random.choices(string.ascii_letters, k=5))
#     #         if s not in self._orbits:
#     #             return s 

#     def _epsilonV(self):
#         d = self.lattice.dim
#         return np.array([1e-7]*d)

#     def addOrbit(self,pos,name):
#         # if name is None:
#         #     name = self._getRandomOrbitName() 
#         if name in self._orbits:
#             raise FermionLatticeError(f"name '{name}' is used. Use others")  
#         orbit = _Orbit(pos=pos,name=name) 
#         orbit.attach2Lattice(self.lattice) 
#         self._orbits[name] = orbit

#     @staticmethod
#     def _getTwoObrbiInterKey(oName1,oName2):
#         return oName1 + "_2_" + oName2

#     def setHopping(self,orbit_i,orbit_j,distance,tij):
#         self.lattice.add_connection(orbit_i, orbit_j, distance) 
#         self._interaction[ self._getTwoObrbiInterKey(orbit_i,orbit_j) ] = tij
#         # self._interaction[ self._getTwoObrbiInterKey(orbit_j,orbit_i) ] = tij.conjugate() 






'''

   PrimaryLattice_SpinlessHamiltonian
                │
                │
            ┌───┴──
            │
 PrimaryLattice_HubbardModel


 

 




'''






















class PrimaryLattice_SpinlessHamiltonian():
    """
    Set Hamiltonian of a lattice model. 
    This class:
    * use lest effort to define the toplogy of a lattice Hamiltonian.
    * contains only connection topology, need not position information. BUT, we contains position information here.
    This class is a basic one for spinless fermion system.
    """    

    def __init__(self,basis):
        self.varMat = VariableTypeChecker(ErrorException = FermionLatticeError)
        self._data = {
            "DC":{},     # 'R':[3D int array], 'cName':str, 'iParams':[], cParam:*
            "DDCC":{},
            "DCDC":{},
        } 
        self._PrimaryBasis = np.array(basis) 
        self.H0 = 0 
        self._orbitNameTable = {} 
        self._orbitPosition = {} 

    def getPrimaryBasis(self):
        return np.array( self._PrimaryBasis )
    
    def getPositionOnLattice(self,index):
        basis = self.getPrimaryBasis() 
        res = np.array([0.,0.,0.]) 
        for i in range(3):
            res += basis[i] * index[i] 
        return res

    def _exportInteraction(self):
        res = [] 
        for cName in self._data:
            for k in self._data[cName]:
                res.append(  dict(self._data[cName][k])  )
        return res 
    
    def setOrbitPosition(self,idx,pos):
        self._orbitPosition[idx] = np.array(pos)
        return self 
    
    def getOrbitPosition(self,idx):
        # print(self._orbitPosition,999)
        return self._orbitPosition[idx] 
    
    def getNumOfSpinlessOrbit(self):
        n = len(self._orbitPosition) 
        if n == 0:
            logging.warn("number of orbit is 0, not set position of orbit?")
        return n 

    # def getNinteraction(self):
    #     return len(self._exportInteraction()) 
    
    def getInteraction(self):
        return self._exportInteraction()
        

    def _orbitName2index(self,nameOrIndex):
        if isinstance(nameOrIndex,numbers.Integral):
            return nameOrIndex
        else:
            i = self._orbitNameTable.get(nameOrIndex,None)
            if i is None:
                i = len(self._orbitNameTable)
                self._orbitNameTable[nameOrIndex] = i 
            return i 

    def _setOrAppend(self,R,cName,iParams0,iParamsR,cParam):
        """set single term WITHOUT h.c.

        Args:
            R (int): 3D integer vector  
            cName (str): DC, DDCC,....
            iParams0 (list): int params, related to current cluster (R=[0,0,0])
            iParamsR (list): int params, related to current cluster (R)
            cParam (complex): value 
        """   
        self.varMat.batchVariableMatch1Type(srcVals=iParams0,desType=numbers.Integral,funName='_setOrAppend') 
        self.varMat.batchVariableMatch1Type(srcVals=iParamsR,desType=numbers.Integral,funName='_setOrAppend') 
        self.varMat.matchTypeRaiseError(srcVal=cParam,desType=numbers.Complex,funName='_setOrAppend') 
        key = "_".join([ str(i) for i in ( list(R) + list(iParams0)+ list(iParamsR) ) ])
        # print('called',R,cName,iParams0,iParamsR,cParam)
        if key not in self._data[cName]:
            self._data[cName][key] = {'R':np.array(R), 'cName':cName, 'iParams0':list(iParams0), 'iParamsR':list(iParamsR),'cParam':cParam}
        else:
            self._data[cName][key]['cParam'] += cParam
        return self 

    def setCdC(self,R,i,j,tij):
        r"""
           :math:`t_{R_i i, R_j j} c^\dagger_{R_i i} c_{R_j j} + h.c.` 
           By default, :math:`{R_i}` is [0]*d. So one need only to give :math:`R_j` by R.

        Args:
            R (int): list of int. represent index of primary cell. 
            i (int): index of orbit in current ([0]*d) cell.
            j (int): index of orbit in Rj
            tij (complex): hopping strength
        """  
        self._setOrAppend(R=R, cName='DC', iParams0=[i],iParamsR=[j], cParam=tij ) 
        return self._setOrAppend(R=[ -v for v in R ], cName='DC', iParams0=[j],iParamsR=[i], cParam=tij.conjugate() )  

    def setCdCdCC(self,R,i1,i2,j1,j2,v):
        r"""
            :math:`v c^\dagger_{R_i i_1} c^\dagger_{R_i i_2} c_{R_j j_1} c_{R_j j_2} + h.c.` 
            By default, :math:`{R_i}` is [0]*d. So one need only to give :math:`R_j` by R. 

        Args:
            R (int): list, :math:`{R_j}`: [int]*d
            i1 (int): index of orbit in current ([0]*d) cell.
            i2 (int): index of orbit in current ([0]*d) cell.
            j1 (int): index of orbit in Rj
            j2 (int): index of orbit in Rj
            v (complex): energy value
        """
        self._setOrAppend(R=R,cName='DDCC', iParams0 = [i1,i2] , iParamsR=[j1,j2], cParam=v ) 
        return self._setOrAppend(R= [ -v for v in R ] ,cName='DDCC', iParams0=[j2,j1], iParamsR=[i2,i1], cParam=v.conjugate() )  
    
    def setCdCCdC(self,R,i1,i2,j1,j2,v):
        r"""
            :math:`v c^\dagger_{R_i i_1} c_{R_i i_2} c^\dagger_{R_j j_1} c_{R_j j_2} + h.c.` 
            By default, :math:`{R_i}` is [0]*d. So one need only to give :math:`R_j` by R. 

        Args:
            R (int): list, :math:`{R_j}`: [int]*d
            i1 (int): index of orbit in current ([0]*d) cell.
            i2 (int): index of orbit in current ([0]*d) cell.
            j1 (int): index of orbit in Rj
            j2 (int): index of orbit in Rj
            v (complex): energy value
        """
        self._setOrAppend(R=R, cName='DCDC', iParams0 = [i1,i2] , iParamsR=[j1,j2], cParam=v ) 
        return self._setOrAppend(R=[ -v for v in R ], cName='DCDC', iParams0=[j2,j1], iParamsR=[i2,i1], cParam=v.conjugate() )  
    
    def __repr__(self) -> str:
        r = ''
        interactions = self._exportInteraction() 
        for inter in interactions:
            line = ''
            iParams = inter['iParams0'] + inter['iParamsR']
            for i,c in enumerate(list(inter['cName'])):
                if c == 'D':
                    dagger = "^+"
                else:
                    dagger = ''
                line += f"C{dagger}_{ iParams[i] }"
            line = "   " + f"{inter['R']} " + line + f": {inter['cParam']}"
            r += line + "\n"
        return r 
        
    def exportLocalHamiltonian(self) -> SpinlessHamiltonian:
        '''return a cluster Hamiltonian, will ignore non-local part'''
        rH = SpinlessHamiltonian() 
        interactions = self._exportInteraction() 
        for inter in interactions:
            # print(777,inter)
            if any( inter['R'][i] != 0 for i in range(3) ):
                continue
            iParams = inter['iParams0'] + inter['iParamsR'] 
            rH._setOrAppend(cName=inter['cName'],iParams=iParams,cParam=inter['cParam'])
        return rH

        # {'R':np.array(R), 'cName':cName, 'iParams0':list(iParams0), 'iParamsR':list(iParamsR),'cParam':cParam}

    def _count_N_orbit(self,interactions=None):
        if interactions is None:
            interactions = self._exportInteraction() 
        count = set() 
        for int in interactions:
            iParams = int['iParams0'] + int['iParamsR']
            for i in iParams:
                count.add(i) 
        idMax = max(count) 
        l = len(count)
        if idMax != l - 1:
            pass # warning!!
        else:
            return idMax + 1  

    def getTmatrix(self,nOrbit=None):
        """return hopping terms
        """        
        interactions = self._exportInteraction() 
        if nOrbit is None:
            nOrbit = self._count_N_orbit(interactions=interactions)
        res = np.zeros((nOrbit, nOrbit),dtype=complex)
        for int in interactions:
            if int['cName'] == 'DC':
                i = int['iParams0'][0] 
                j = int['iParamsR'][0] 
                res[i][j] += int['cParam']
        return res 

        



        


    
class PrimaryLattice_HubbardModel(PrimaryLattice_SpinlessHamiltonian):
    """
        PrimaryLattice of Hubbard model. Contains t,mu,U

    """ 

    def setOrbitPosition(self,idx,pos):
        super().setOrbitPosition( idx=idx*2, pos=pos)
        super().setOrbitPosition( idx=idx*2+1, pos=pos)
        return self 
    
    # def getOrbitPosition(self,idx):
    #     return super().getOrbitPosition(idx=idx*2)
  
    def setHopping(self,R,orbit_i,orbit_j,tij):
        self.setCdC(R=R,i=orbit_i*2,j=orbit_j*2,tij=tij) 
        self.setCdC(R=R,i=orbit_i*2+1,j=orbit_j*2+1,tij=tij) 
        return self 

    def setOnSide(self,orbit_i,m):
        R = [0,0,0] 
        self.varMat.matchTypeRaiseError(srcVal=m,desType=numbers.Real,funName='setOnSite') 
        self.setCdC(R=R,i=orbit_i*2,j=orbit_i*2,tij=m/2.0) 
        self.setCdC(R=R,i=orbit_i*2+1,j=orbit_i*2+1,tij=m/2.0)
        return self  

    def setCoulombU(self,orbit_i:int,U:float):
        r"""
            :math:`U n_{R_0 i} n_{R_0 j}` 

        Args:
            orbit_i (int): orbit index
            U (float): U
        """
        self.varMat.matchTypeRaiseError(srcVal=U,desType=numbers.Real,funName='setCoulombU')
        i = orbit_i * 2
        j = i + 1
        return self._setOrAppend(R=[0,0,0],cName='DCDC',iParams0= [i,i], iParamsR = [j,j],cParam=U)
    
    def setInterV(self,R,orbit_i:int,orbit_j:int,V:float):
        r"""
            :math:`V n_i n_j = V ( n_{i\uparrow} + n_{i\downarrow} ) ( n_{j\uparrow} + n_{j\downarrow} )`
            where orbit_i is in current cluster and orbit_j is R

        Args:
            R (int): R_j
            orbit_i (int): index of site
            orbit_j (int): index of site
            V (float): strength

        Returns:
            _type_: _description_

        Yields:
            _type_: _description_
        """
        self.varMat.matchTypeRaiseError(srcVal=V,desType=numbers.Real,funName='setInterV') 
        for di in (0,1):
            for dj in (0,1):
                self._setOrAppend(R=R,cName='DCDC',
                                  iParams0= [orbit_i*2+di,orbit_i*2+di], 
                                  iParamsR = [orbit_j*2+dj,orbit_j*2+dj],
                                  cParam=V,
                                  )
        return self 
 







class IntegerMesh():

    @staticmethod
    def get_all_inside_parallelepiped(a1,a2,a3):
        """reture all integer points inside a parallelepiped which has one vertex at the origin and arms defined by a1,a2,a3.
        For 2D case, set a3=[0,0,1]. And for 1D case also set a2=[0,1,0].

        Args:
            a1 (int): arms of parallelepiped
            a2 (int): arms of parallelepiped
            a3 (int): arms of parallelepiped
        """   
        A = np.array([ 
            [ a1[0], a2[0], a3[0] ],
            [ a1[1], a2[1], a3[1] ],
            [ a1[2], a2[2], a3[2] ],
              ])
        vecR = [ a1[0]+a2[0]+a3[0], a1[1]+a2[1]+a3[1], a1[2]+a2[2]+a3[2] ]      
        R = ( vecR[0]**2 + vecR[1]**2 + vecR[2]**2 )**0.5 
        L = int(2*R) 
        res = []
        for i in range(-L,L):
            for j in range(-L,L):
                for k in range(-L,L):
                    b = np.array([i,j,k]) 
                    x = np.linalg.solve(A, b)
                    if not any(  ( not ( (0 <= xi) and (xi<1) ))  for xi in x ):
                        res.append(b) 
        return res  
    
    @staticmethod
    def iterateAround(pos):
        for i in (1,-1):
            for j in (1,-1):
                for k in (1,-1):
                    yield pos[0]+i,pos[1]+j,pos[2]+k 

    @staticmethod
    def posInList(pos,posList):
        return any( ((pos[0]==p[0]) and (pos[1]==p[1]) and(pos[2]==p[2])) for p in posList)
            



# class orbitConfig():

#     def __init__(self,basis):
#         self.basis = basis 
#         self._orbitPos = {}   

#     def setOrbit(self,index,pos):
#         self._orbitPos[index] = np.array(pos)  

#     def getNumOrbit(self):
#         return len(self._orbitPos) 


class _MapSuperLattice():
    '''
    tool for find mappling between lattice
    '''

    def __init__(self,superIndex,nOrbitInPrimary):
        self.superIndex = np.array(superIndex) 
        self.n = nOrbitInPrimary
        #------- 
        self._primaryCells = IntegerMesh.get_all_inside_parallelepiped(*self.superIndex) # list of int point, each represent position of primary cell.
        self._inverTable = { tuple(self._primaryCells[i]):{"idx":i}  for i in range(len(self._primaryCells))}

    def getPrimaryIndexPosition(self,pid):
        return self._primaryCells[pid] 

    def getPrimaryCellID(self,pos):
        return self._inverTable[ tuple(pos) ]['idx']
    
    def get_which_super_is_this_primary_in(self,pos):
        r"""For any given integer Vector p 
          :math:`p = \sum_i x_i * S_i + p`

        Args:
            pos (_type_): _description_

        Returns:
            position_of_superCell (unit of supIndex), position_of_primaryCell
        """        
        A = self.superIndex.transpose() 
        x = np.linalg.solve(A, np.array(pos) )
        sPos = [ math.floor(x[i]) for i in range(3)]
        pPos = np.array(pos) - sum(np.array([sPos[i] * self.superIndex[i] for i in range(3)])) 

        # print(f'''
        #  decompose p={pos}, 
        #  s = {sPos},
        #  p = {pPos}, 
        #  s*i = {sum(np.array([sPos[i] * self.superIndex[i] for i in range(3)])) }
        # ''')
        return tuple(sPos), tuple(pPos)
    
    def getOrbitID_inSuperCell(self,priCellPos,oid):
        pid = self.getPrimaryCellID(priCellPos)
        return pid * self.n + oid
    
    def getOrbitID_inSuperCell_inverse(self,OID):
        ''' 
        The inverse function getOrbitID_inSuperCell. 
        For a given orbit index in supercell, return the original oid in primary cell and the position of Primary cell.
        '''
        oid = OID % self.n 
        pid = OID // self.n
        pos = self._primaryCells[pid] 
        return pos,oid  


class SuperLatticeHamiltonian():
    """
    Make super-lattice Hamiltonian by PrimaryHamiltonian
    只能计算14类格子中的7类: 简单(x5)，三角(x1)和六角(x1)。拓扑上等价于简单立方。
    """    

    def __init__(self,priHam:PrimaryLattice_SpinlessHamiltonian,superLatticeIndex):
        self._priHam = priHam
        self.superLatticeIndex = np.array(superLatticeIndex)
        self.mapper = _MapSuperLattice( self.superLatticeIndex, self._priHam.getNumOfSpinlessOrbit() )
        #------------------
        self.cache = {}


    def _getTranferPrimaryCell(self,pCells,R):
        R = np.array(R)
        return [ np.array(p) + R for p in pCells ]

    def _analyzeAll(self,superIndex):
        superIndex = np.array( superIndex )
        # nOrbits = self._priHam.getNumOfSpinlessObrit()
        mapper = self.mapper#_MapSuperLattice(superIndex,nOrbits)
        # ----- handle Hamiltonian terms in the primary cell 
        priH_terms = self._priHam.getInteraction() 
        supLattice = {}
        priCells = np.array( IntegerMesh.get_all_inside_parallelepiped(*superIndex ) )
        for p_this in priCells:
            for inter in priH_terms:
                p_that = p_this + inter['R']
                that_sPos,that_pPos = mapper.get_which_super_is_this_primary_in(p_that)
                # print(f"p_that={p_that}",f"that_sPos={that_sPos}",f"that_pPos={that_pPos}")
                if that_sPos not in supLattice:
                    supLattice[ that_sPos ] = {
                        'H' : PrimaryLattice_SpinlessHamiltonian( self._priHam.getPrimaryBasis() ), 
                        'supIndex': that_sPos, # in the basis of superIndex
                        'priIndex': sum(np.array([that_sPos[i] * superIndex[i] for i in range(3)])) ,# in the basis of 
                    }
                iParams0 = [mapper.getOrbitID_inSuperCell(priCellPos=p_this,oid=i) for i in inter['iParams0']]
                iParamsR = [mapper.getOrbitID_inSuperCell(priCellPos=that_pPos,oid=i) for i in inter['iParamsR']]
                # print(p_this,that_pPos,iParams0,iParamsR)
                supLattice[that_sPos]['H']._setOrAppend(
                    R=that_sPos,
                    cName=inter['cName'],
                    iParams0= iParams0 ,
                    iParamsR=iParamsR,
                    cParam=inter['cParam'],
                    )
                # #--------------------- debug ------------------------------------------
                # print('sssss')
                # if that_sPos[0] == 0 and that_sPos[1] == 0 and that_sPos[2] == 0:
                #     print(1,that_sPos,inter['cName'],iParams0,iParamsR,inter['cParam'])
                # # -------------- end debug --------------------------
        return supLattice
    
    def _get_SuperlatticeConfiguration(self):
        superIndex = self.superLatticeIndex
        key = tuple(np.array(superIndex).reshape(-1))
        if key not in self.cache:
            self.cache[key] = self._analyzeAll(superIndex)
        return self.cache[key]

    def get_ClusterH(self)->SpinlessHamiltonian:
        supLat = self._get_SuperlatticeConfiguration() 
        priH = supLat[tuple([0,0,0])]['H']
        cH = priH.exportLocalHamiltonian()
        return cH
    
    def abstractT_from_primaryH():
        pass 
    
    def _getTq(self,q):
        q = np.array(q)
        supLat = self._get_SuperlatticeConfiguration() 
        res = None
        for sup in supLat:
            if sup == tuple([0,0,0]):
                continue
            lat = supLat[sup]
            H = lat['H'] 
            posDelta = H.getPositionOnLattice( lat['priIndex'] )
            exp = np.exp( 1j * sum(q * posDelta) )
            if res is None:
                res = exp * H.getTmatrix() 
            else:
                res = res + exp * H.getTmatrix()
        return res 

    def getTq(self,q:list[int],index: list[int] | None = None):
        r"""          
            :math:`T_q=\sum_{\Delta}e^{i \boldsymbol{q} \cdot \boldsymbol{\Delta} } t(\Delta)`, where
            :math:`\Delta=\boldsymbol{R}-\boldsymbol{0}`

        Args:
            q (list[int]): k vector
            index (list[int] | None, optional): _description_. Defaults to None.
        """  
        T = self._getTq(q) 
        if index is None:  
            return T 
        else:
            return T[np.ix_(index,index)]
        
    def getNumOrbitInCell(self)-> int:
        """Total numer of (spinless) orbits in a primary cell (or say basis cell)

        Returns:
            int: number of orbits
        """        
        
        return self._priHam.getNumOfSpinlessOrbit()
    
    def getCLusterSize(self):
        '''
        :math:`V_{lattic}/V_{cell}`  
        '''
        if not hasattr(self,"_INTERNAL_SIZEL"):   
            b = np.cross( self.superLatticeIndex[0], self.superLatticeIndex[1] )
            v = abs(sum(b * self.superLatticeIndex[2]))
            self._INTERNAL_SIZEL =  int( v + 0.0001 )
        return self._INTERNAL_SIZEL  

    def getAbsPositionOfOrbit(self,pid:int,oid:int)->Vector:
        """_summary_

        Args:
            pid (int): index of primary cell
            oid (int): index of orbit in primary cell 

        Returns:
            Vector: absolute position of a given orbit in real space
        """   
        posCell = self.mapper.getPrimaryIndexPosition(pid) 
        basis = self._priHam.getPrimaryBasis()  
        absPosCell = basis[0] * posCell[0] + basis[1] * posCell[1] + basis[2] * posCell[2]  
        dx = self._priHam.getOrbitPosition(idx=oid) 
        return absPosCell + dx
    
    def getOrbitIndexInSuperCell(self,pid:int,oid:int)->int:
        """

        Args:
            pid (int): index of primary-cell
            oid (int): index of orbit in primary-cell 

        Returns:
            int: orbit index in super-cell.
        """  
        n = self._priHam.getNumOfSpinlessOrbit() 
        return pid * n + oid        
    
    
    # def getAbsPositionOfOrbit(self,Oid:int)->Vector:
    #     """For a given index of orbit in the super-lattice, return the absolute position in realspace. 

    #     Args:
    #         Oid (int): index of orbit in super-lattice. Not be confused of Oid and oid. oid is in index of orbit in a primary cell, and Oid is the index in super-lattice. 

    #     Returns:
    #         Vector: position in real-space 
    #     """    
    #     posCell,oid = self.mapper.getOrbitID_inSuperCell_inverse(OID=Oid)   
    #     basis = self._priHam.getPrimaryBasis()  
    #     absPosCell = basis[0] * posCell[0] + basis[1] * posCell[1] + basis[2] * posCell[2]  
    #     dx = self._priHam.getOrbitPosition(idx=oid) 
    #     return absPosCell + dx



        



     

  

        
        
        












        






        

        