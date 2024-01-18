import numpy as np 
from .import GaussLegendreIntegration
from .retardedGreenfunction import RetardedGreenFunction



class GreenFuncZ():

    def __init__(self,tMax:float,tN:int,rGObj:RetardedGreenFunction):
        r"""
            :math:`G_{ij}(z) = \int^{t_{Max}}_0 dt e^{izt} G_{ij}(t)` 

        Args:
            tMax (float): upper limit for integration
            tN (int): Num of points for integration
            rGObj (RetardedGreenFunction): _description_
        """        
        self.tMax = tMax 
        self.tN = tN 
        self.rGObj = rGObj # retarded GF object
        self.I = GaussLegendreIntegration() 
        self.tList,self.W = self.I.getzw(n=self.tN,z1=0,z2=self.tMax)

    def Gz(self,i,j,zList):
        GT = self.rGObj.G(i=i,j=j,Tlist=self.tList) 
        Gz = []
        for z in zList:
            g = 0 
            for i in range(len(self.tList)):
                g += GT[i] * np.exp(1j*z*self.tList[i])  * self.W[i]
            Gz.append(g) 
        return np.array(Gz)  
    
    def G_Omega(self,i,j,OmegaList,eta):
        zList = OmegaList + 1j*eta 
        return self.Gz(i=i,j=j,zList=zList)
    
    def GzMatrix(self,zList:list,index:list):
        r"""
            [G(z1),G(z2),...] where each G(zi) is a LxL matrix. 
            
        Args:
            zList (list): z for G(z)
            index (list): The range of i and j for G_{ij}. The length should be L.

        Returns:
            list: 
        """            
        # index = [] define the range of the index i,j in G_{ij}
        d = len(index)
        GM = np.zeros((len(zList),d,d) , dtype=np.complex128)
        # for i in range( d ):
        #     for j in range(i,d):
        #         GM[:,i,j] = self.Gz( i = index[i], j = index[j], zList=zList )  
        #         if i!=j:
        #             GM[:,j,i] = np.conjugate(GM[:,i,j])
        # return GM
        for i in range( d ):
            for j in range(d):
                GM[:,i,j] = self.Gz( i = index[i], j = index[j], zList=zList )  # G(i,j) and G(j,i) is not conjugate !? 
        return GM
