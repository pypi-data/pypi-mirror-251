# -*- coding: UTF-8 -*-

import numbers
from collections import defaultdict
from ..qubitEncoding import FermionEncoding
from ...utils import VariableTypeChecker



class FermionHamiltonianError(Exception):pass 





class SpinlessHamiltonian():
    r"""set a general Hamiltonian:
        :math:`H=\sum_{ij} c^\dagger_i c_j +\sum_{ijkl} c^\dagger_i c^\dagger_j c_k c_l` 

    """    

    def __init__(self):
        self._data = {
            "DC":{},   
            "CC":{},
            "DD":{},
            "DDCC":{},
            "DCDC":{},
            } 
        self.H0 = 0 
        self.varMat = VariableTypeChecker( FermionHamiltonianError )

    def getCountN(self):
        '''count total number of sites'''
        l = []
        for k in self._data:
            for kk in self._data[k]:
                l += list(self._data[k][kk]['iParams'])
        r = 0 
        for i in l:
            r = max(i,r) 
        return r + 1

    def _setOrAppend(self,cName,iParams,cParam):
        """set single term WITHOUT h.c.

        Args:
            cName (str): DC, DDCC,....
            iParams (list): int params
            cParam (complex): value 
        """       
        self.varMat.batchVariableMatch1Type(srcVals=iParams,desType=numbers.Integral,funName='_setOrAppend') 
        self.varMat.matchTypeRaiseError(srcVal=cParam,desType=numbers.Complex,funName='_setOrAppend') 
        key = "_".join([ str(i) for i in iParams ])
        if key not in self._data[cName]:
            self._data[cName][key] = {'iParams':list(iParams),'cParam':cParam}
        else:
            self._data[cName][key]['cParam'] += cParam
        return self 
    
    # def getNinteraction(self):
    #     '''return num of terms in H'''
    #     res = 0 
    #     res += len(self._data['DC'])   \
    #         +  len(self._data['CC'])   \
    #         +  len(self._data['DD'])   \
    #         +  len(self._data['DDCC']) \ 
    #         +  len(self._data['DCDC']) \ 
    #         + 1 # constant term 
    #     return res  
        


    def set_CdC(self,i,j,val):
        """
        term:
           v C^+_i C_j + h.c.

        Args:
            i (int): site index
            j (int): site index
            val (complex): coefficient
        """
        self._setOrAppend("DC",iParams=[i,j],cParam=val)
        self._setOrAppend("DC",iParams=[j,i],cParam=val.conjugate()) 
        return self 

    def set_CC(self,i,j,val):
        """
        term:
           v C_i C_j + h.c.

        Args:
            i (int): site index
            j (int): site index
            val (complex): coefficient
        """
        self._setOrAppend("CC",iParams=[i,j],cParam=val)
        self._setOrAppend("DD",iParams=[j,i],cParam=val.conjugate()) 
        return self

    def set_CdCdCC(self,i,j,k,l,val):
        """
        term:
           v C^+_i C^+_j C_k C_l + h.c.

        Args:
            i (int): site index
            j (int): site index
            k (int): site index
            l (int): site index
            val (complex): coefficient
        """
        self._setOrAppend("DDCC",iParams=[i,j,k,l],cParam=val)
        self._setOrAppend("DDCC",iParams=[l,k,j,i],cParam=val.conjugate()) 
        return self

    def set_CdCCdC(self,i,j,k,l,val):
        """
        term:
           v C^+_i C_j C^+_k C_l + h.c.

        Args:
            i (int): site index
            j (int): site index
            k (int): site index
            l (int): site index
            val (complex): coefficient
        """
        self._setOrAppend("DCDC",iParams=[i,j,k,l],cParam=val)
        self._setOrAppend("DCDC",iParams=[l,k,j,i],cParam=val.conjugate()) 
        return self

    def setOnSiteEnergy(self,i,m):
        r"""
            :math:`m * n_i`

        Args:
            i (int): site index
            m (float): onsite energy
        """        
        self.varMat.matchTypeRaiseError(srcVal=m,desType=numbers.Real,funName='setOnSiteEnergy')
        self._setOrAppend("DC",iParams=[i,i],cParam=m)
        return self

    def setHopping(self,i:int,j:int,tij):
        r"""
          :math:`t_{ij} c^+_i c_j + h.c.`

        Args:
            i (int): site index  
            j (int): site index  
            tij (complex): hopping energy  
        """       
        return self.set_CdC(i,j,tij)  

    def setCoulomb(self,i:int,j:int,U:float):
        r"""
            :math:`U n_i n_j` 

        Args:
            i (int): site index
            j (int): site index
            U (float): U
        """
        self.varMat.matchTypeRaiseError(srcVal=U,desType=numbers.Real,funName='setCoulomb')
        return self._setOrAppend(cName='DCDC',iParams=[i,i,j,j],cParam=U)
    
    def _exportFermionOperator(self):
        r = [self.H0]
        for cName in self._data:
            if len(self._data[cName]) == 0:
                continue
            cs = list(cName)
            for key in self._data[cName]:
                line = [ self._data[cName][key]['cParam'] ]
                iParams = self._data[cName][key]['iParams']
                for i in range(len(cs)):
                    line.append([cs[i],iParams[i]])
                r.append(line)
        return r
    
    def __repr__(self) -> str:
        lines = self._exportFermionOperator() 
        r = 'Fermion-type (spinless) Hamiltonian:\n' 
        r += f"   H0 = {lines[0]}\n"
        for line in lines[1:]:
            val = line[0] 
            cNamePrint = ''
            for c in line[1:]:
                o,i = c 
                dagger = "^+" if o == 'D' else ''
                cNamePrint += f"C{dagger}_{i} "
            r += f"   {cNamePrint}: {val} \n"
        return r 

    def exportPauliOperator(self,encoding):
        if hasattr(encoding, '__name__'):
            raise FermionHamiltonianError("input [encoding] must be an instance, not a class")
        if not isinstance(encoding,FermionEncoding):
            raise FermionHamiltonianError(f"encoding must by a subclass of [{FermionEncoding}]")
        container = encoding.get0() 
        lines = self._exportFermionOperator() 
        container.addConstant( lines[0] )
        for line in lines[1:]:
            val = line[0]
            One = encoding.get1()
            for c in line[1:][-1::-1]:
                o,i = c 
                if o == 'D':
                    p = encoding.cd(i) 
                elif o =='C':
                    p = encoding.c(i)
                else:
                    raise FermionHamiltonianError("???")
                One = p * One 
            container = container + val * One
        return container  
                
                
class SpinfulHamiltonian():
    r"""set a general Hamiltonian: :math:`H=H_0+H_1` where

        :math:`H_0=\sum_{ij}\sum_{\sigma\sigma'} c^\dagger_{i\sigma} c_{j\sigma'}`  
        and  
        :math:`H_1=\sum_{ijkl}\sum_{\alpha\beta\gamma\delta} c^\dagger_{i\alpha} c^\dagger_{j\beta} c_{k\gamma}c_{l\delta}`

    This Hamiltonian is made of `SpinlessHamiltonian` with mapping spin-up (spin-down) into even (odd) site.

        

        
    """   
    # :math:`H_1=\sum_{ijkl} c^\dagger_i c^\dagger_j c_k c_l ` 

    def __init__(self):
        self.spinlessHam = SpinlessHamiltonian() 
        self.varMat = VariableTypeChecker( FermionHamiltonianError )

    def setHopping(self,i:int,j:int,tij:complex):
        r"""
            :math:`t_{ij} \sum_{i,j,\sigma} c^+_{i\sigma} c_{j\sigma} + h.c.` 

        Args:
            i (int): site index.
            j (int): site index.
            tij (complex): _description_

        """   
        self.spinlessHam.setHopping(i=2*i,j=2*j,tij=tij)
        self.spinlessHam.setHopping(i=2*i+1,j=2*j+1,tij=tij)
        return self  
    
    def setOnSiteEnergy(self,i,m):
        r"""
            :math:`m  \sum_{\sigma} c^+_{i\sigma}c_{i\sigma}` 

        Args:
            i (_type_): site index
            m (_type_): energy

        Returns:
            self: 
        """        
        self.spinlessHam.setOnSiteEnergy(i=2*i,m=m)
        self.spinlessHam.setOnSiteEnergy(i=2*i+1,m=m)
        return self 
    
    def setCoulombU(self,i:int,U:float):
        r"""
            :math:`U n_{i\uparrow} n_{i\downarrow}` 

        Args:
            i (int): site index
            U (float): U

        Returns:
            self:    
        """ 
        self.spinlessHam.setCoulomb(i=2*i,j=2*i+1,U=U) 
        return self 
    
    def setCoulombV1(self,i:int,j:int,V:float):
        r"""
           
           :math:`V n_i n_j`, where :math:`n_i = n_{i\uparrow} + n_{i\downarrow}` 

        Args:
            i (int): site index
            j (int): site index 
            V (float): V 
        """
        self.spinlessHam.setCoulomb(i=2*i,j=2*j,U=V)
        self.spinlessHam.setCoulomb(i=2*i,j=2*j+1,U=V)
        self.spinlessHam.setCoulomb(i=2*i+1,j=2*j,U=V)
        self.spinlessHam.setCoulomb(i=2*i+1,j=2*j+1,U=V)
        return self  
    
    def exportPauliOperator(self,encoding):
        return self.spinlessHam.exportPauliOperator(encoding) 








    



                        

                
            








