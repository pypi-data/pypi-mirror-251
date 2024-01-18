from __future__ import annotations
import numpy as np 
from .frequencyGreenf import GreenFuncZ
from .import SuperLatticeHamiltonian as supH
import typing

Matrix = typing.Any
Vector = typing.Any



class LattGreenFuncError(Exception):pass 


class LatticeGreenFunction():

    def __init__(self,GZ:GreenFuncZ,supH:supH):
        self.GzObj = GZ
        self.supH = supH

    def _getIndexByindex(self,index):
        '''index defined the studied orbits in primary-cell, while Index match super-lattice cell'''
        L = self.supH.getCLusterSize()
        Index = []
        for pid in range(L):
            for oid in index:
                Oid = self.supH.getOrbitIndexInSuperCell(pid=pid,oid=oid)
                Index.append(Oid)
        return Index 

    def getGqMatrix(self,q:Vector, GcInv:Matrix,index:list[int] | None = None)->Matrix:     
        r"""
            :math:`\boldsymbol{G}^{-1}(\boldsymbol{q},\omega)=\boldsymbol{G}^{-1}_{\text{cluster}}(\boldsymbol{q},\omega)-\boldsymbol{T}_{\boldsymbol{q}}`

        Args:
            q (Vector): k vector
            GcInv (Matrix): inverse matrix of the matrix of Green's function of a single cluster
            index (list[int] | None, optional): if None, dim(G) = size of super cell. 

        Returns:
            Matrix: _description_
        """   
        if index is None:
            index = list(range(0,self.supH.getNumOrbitInCell()))
        lG = len(GcInv)
        lidx = len(index)
        L = self.supH.getCLusterSize()
        if lG != lidx*L:
            raise LattGreenFuncError(f"input size dismatch, dim(Gz)={lG} while dim(index)={lidx}")
        Index = self._getIndexByindex(index)
        Tq = self.supH.getTq(q=q,index=Index)
        Ginv = GcInv - Tq
        return np.linalg.inv(Ginv)
    
    def getGqMatrixList(self,q:Vector, zList:list|None = None, GcList:list[Matrix]|None=None,index:list[int] | None = None)->list[Matrix]:
        """Generate list of Gq matrix. One need to input zList or GcList, NOT both. This subroution is used to consider different :math:`\omega.
        Notice that z =:math:`\omega+i\eta`

        Args:
            q (Vector): _description_
            zList (list | None, optional): defines :math:`\omega+i\eta`. Defaults to None.
            GcList (list[Matrix] | None, optional): Cluster Green's function. Defaults to None.
            index (list[int] | None, optional): index of orbit. Defaults to None.

        Returns:
            list[Matrix]: _description_
        """     
        if (zList is not None) and (GcList is not None):
            raise LattGreenFuncError("zList and GcList cannot be given in both")
        if GcList is None:
            Index = self._getIndexByindex(index)
            GcList = self.GzObj.GzMatrix(Zlist=zList,index=Index) 
        res = [] 
        for g in GcList:
            ginv = np.linalg.inv(g)
            res.append( self.getGqMatrix(q=q,GcInv=ginv, index=index)   ) 
        return res   

    def _getSingleGk(self,k,GqList,index):
        res = [0]*len(GqList)
        l = len(index) 
        d = len(GqList[0]) 
        def x(i):
            oid = index[ i % l ]
            pid = i // l  
            return self.supH.getAbsPositionOfOrbit(pid=pid,oid=oid) 
        for i in range(d):
            xi = x(i) 
            for j in range(d):
                xj = x(j) 
                for gi in range(len(GqList)):
                    res[gi] += np.exp( -1j*sum(k*(xi-xj)) ) * GqList[gi][i][j] 
        L = self.supH.getCLusterSize()
        return np.array(res)/L


    def getGkList(self, k:Vector,zList:list[complex]|None = None, GcList:list[Matrix]|None=None, index:list[int] | None = None ) ->list[complex]:  
        r"""
            :math:`g(\boldsymbol{k},\omega) = \frac{1}{L} \sum_{ij} e^{-i \boldsymbol{k}\cdot \boldsymbol{k}( \boldsymbol{x}_i - \boldsymbol{x}_j )} G_{ij}(\boldsymbol{k},\omega)` where

            :math:`L` is the size of the cluster

        Args:
            k (Vector): position in k-space
            zList (list[complex] | None, optional): defines :math:`\omega+i\eta`. Defaults to None.
            GcList (list[Matrix] | None, optional): Matrix of Green's function of the reference cluster. It is a list because of different omega.
            index (list[int] | None, optional): The calculation can only include part of orbitals. :math:`index` defines the set of orbits of consideration.

        Returns:
            complex: Green's function in 1st Brillouin zone.
        """   
        GqMatrixList = self.getGqMatrixList(q=k,zList=zList,GcList=GcList,index=index)
        index = list(range(0,self.supH.getNumOrbitInCell())) if index is None else index
        # res = []
        # for Gq in GqMatrixList:
        #     gk = self._getSingleGk(k=k,Gq=Gq,index=index) 
        #     res.append(gk) 
        # return res 
        return self._getSingleGk(k=k,GqList=GqMatrixList,index=index)


    @staticmethod
    def _vecRange(v1,v2,n):
        dv = (v2-v1) / n 
        return [ v1 + dv*i for i in range(n)] 

    def getDensityOfState_batchK(self,kPoints:list[Vector],OmegaPoints:list[float],eta:float,index:list[int] = None)->Matrix:       
        r""" return a 2D Matrix. 
               horizontal: k points
               vertical: :math:`\omega` points. max at top, min at bottom

        Args:
            kPoints (list[Vector]): k-points
            OmegaPoints (list[float]): list of :math:`\omega`
            eta (float): artificial broadening


        Returns:
            Matrix: 2D array, can be used for plot directly 
        """    
        kList = kPoints
        L = self.supH.getCLusterSize()
        Index = []
        for pid in range(L):
            for oid in index:
                Oid = self.supH.getOrbitIndexInSuperCell(pid=pid,oid=oid)
                Index.append(Oid)
        GcList = self.GzObj.GzMatrix(zList = np.array(OmegaPoints)+1j*eta,index=Index)  
        G2D = [] 
        for k in kList:
            GkList = self.getGkList(k=k,GcList=GcList,index=index) # omega acending
            GkList = GkList[-1::-1] # omega decending
            G2D.append(GkList) 
        resG = np.array(G2D).transpose()
        rho = - resG.imag / np.pi
        return rho 




    # def getDensityOfState(self,kPoints:list[Vector],OmegaPoints:list[float],eta:float,kMesh:list|int,index:list[int] = None)->Matrix:       
    #     r""" return a 2D Matrix. 
    #            horizontal: k points
    #            vertical: :math:`\omega` points. max at top, min at bottom

    #     Args:
    #         kPoints (list[Vector]): representative points
    #         OmegaPoints (list[float]): list of :math:`\omega`
    #         eta (float): artificial broadening
    #         kMesh (list | int): How many sampling point between each two k-points. If input int, used for all. If input list, length must match kPoints to represent each mesh, that is len(kMesh)=len(kPoints)-1.

    #     Returns:
    #         Matrix: 2D array, can be used for plot directly 
    #     """    
    #     lk = len(kPoints) 
    #     if isinstance(kMesh,int):
    #         kMesh = [kMesh]*(lk-1) 
    #     kList = []
    #     for i in range(len(kMesh)):
    #         kList += self._vecRange(v1=np.array(kPoints[i]),v2=np.array(kPoints[i+1]),n=kMesh[i])
    #     L = self.supH.getCLusterSize()
    #     Index = []
    #     for pid in range(L):
    #         for oid in index:
    #             Oid = self.supH.getOrbitIndexInSuperCell(pid=pid,oid=oid)
    #             Index.append(Oid)
    #     GcList = self.GzObj.GzMatrix(zList = np.array(OmegaPoints)+1j*eta,index=Index)  
    #     G2D = [] 
    #     for k in kList:
    #         GkList = self.getGkList(k=k,GcList=GcList,index=index) # omega acending
    #         GkList = GkList[-1::-1] # omega decending
    #         G2D.append(GkList) 
    #     resG = np.array(G2D).transpose()
    #     rho = - resG.imag / np.pi
    #     return rho 
          
    def getDensityOfState(self,kPoints:list[Vector],OmegaPoints:list[float],eta:float,kMesh:list|int,index:list[int] = None)->Matrix:       
        r""" return a 2D Matrix. 
               horizontal: k points
               vertical: :math:`\omega` points. max at top, min at bottom

        Args:
            kPoints (list[Vector]): representative points
            OmegaPoints (list[float]): list of :math:`\omega`
            eta (float): artificial broadening
            kMesh (list | int): How many sampling point between each two k-points. If input int, used for all. If input list, length must match kPoints to represent each mesh, that is len(kMesh)=len(kPoints)-1.

        Returns:
            Matrix: 2D array, can be used for plot directly 
        """    
        lk = len(kPoints) 
        if isinstance(kMesh,int):
            kMesh = [kMesh]*(lk-1) 
        kList = []
        for i in range(len(kMesh)):
            kList += self._vecRange(v1=np.array(kPoints[i]),v2=np.array(kPoints[i+1]),n=kMesh[i])
        return self.getDensityOfState_batchK(kPoints=kList,OmegaPoints=OmegaPoints,eta=eta,index=index) 


