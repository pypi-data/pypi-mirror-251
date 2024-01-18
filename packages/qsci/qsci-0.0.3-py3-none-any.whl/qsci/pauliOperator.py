from __future__ import annotations
# import logging
import array
import numbers
import numpy as np 
from collections import defaultdict
from .utils import isqdeployer
PauliHamiltonian = isqdeployer.utils.PauliHamiltonian
# from deployer.utils.pauliHamiltonian import PauliHamiltonian


class pauliOperatorError(Exception):pass 




class PauliGroupElement1():    
    """ element in G1
    support multiplexing with +1,-1,+1j,-1j and other G1

    Args:
        Type (int): 0,1,2,3 for I,X,Y,Z respectivily
"""      
    # target operator
    _P = array.array('B', (0,1,2,3,   1,0,3,2,   2,3,0,1,   3,2,1,0 ))
    # target factor, store (1j)**i  
    _F = array.array('B', (0,0,0,0,   0,0,1,3,   0,3,0,1,   0,1,3,0 ))

    def __init__(self,Type:int):  
        if Type not in [0,1,2,3]:
            raise pauliOperatorError(f"Type must in [0,1,2,3]. This type = {Type}")
        self.Type = Type 
        self.n1j = 0 # factor contains 2 parts. This record (1j)**i

    def copy(self):
        new = self.__new__(self.__class__)
        new.Type = self.Type
        new.n1j = self.n1j
        return new 
    
    def getType(self):
        return self.Type

    def getTN(self):
        return self.Type,self.n1j
    
    @classmethod
    def _mulMap(cls,a:int,b:int):
        k = a*4+b
        return cls._P[k],cls._F[k]
    
    def __mul__(self,other,r=False):
        new = self.copy() 
        if type(other) is type(self):
            if r:
                a,b = other.Type, self.Type 
            else:
                a,b = self.Type, other.Type
            P,F = self._mulMap(a,b)
            new.Type = P 
            new.n1j = ( self.n1j + other.n1j + F ) % 4
            return new 
        else: 
            if other == 1:
                pass 
            elif other == -1:
                new.n1j += 2
            elif other == 1j:
                new.n1j += 1
            elif other == -1j:
                new.n1j +=  3    
            else: 
                raise pauliOperatorError(f"illegal operation multiplex between [{self.__class__.__name__}] and {other}")
            new.n1j = new.n1j % 4
            return new
        
    def __rmul__(self,other):
        return self.__mul__(other,r=True)
    
    def __pow__(self,n:int):
        assert not isinstance(n, numbers.Integral)
        new = self.copy() 
        if n < 0:
            assert False
        elif n == 0:
            return new 
        else: 
            for _ in range(n-1):
                new = new * self 
            return new 

    def __repr__(self):
        o = ['I','X','Y','Z'][self.Type]
        f = ['','i','-','-i'][self.n1j]
        r = f"{f}{o}"
        return r.rjust(3, ' ')
    
    def _operatorHash(self) -> int:
        """hash of operator, without factor part

        Returns:
            int: hash value
        """        
        return self.Type
    
    def __hash__(self) -> int:
        return self._operatorHash() 
    
    def getmatrix(self):
        m = [
            [[1,0],[0,1]],
            [[0,1],[1,0]],
            [[0,-1j],[1j,0]],
            [[1,0],[0,-1]],
        ]
        return np.array(m[self.Type]) * (1j**self.n1j)
    

class PauliGroupElementn():
    """PauliGroun for n qubits, G(n)

    Args:
        elements (tuple): (k,i), where 
        i represents index of qubit, 
        k can be int in [0,1,2,3] to represent [I,X,Y,Z] or G(1) element
    """     

    def __init__(self,elements):  
        oList,n1j = self._pharseElement(elements)
        self.Type = self._List2Num( oList )
        self.n1j = n1j

    @staticmethod
    def _pharseElement(elements):
        r = [] 
        n1j = 0
        for e in elements:
            k,i = e
            if type(k) is PauliGroupElement1:
                t,n = k.getTN()
                k,n1j = t,n1j+n  
            if i > len(r) - 1:
                r += [0]*( i - len(r) ) 
                r.append(k)  
            else:
                r[i] = k 
        return r, n1j%4
    
    @classmethod
    def intbyCoreValue(cls,Type,n1j):
        new = object.__new__(cls) 
        new.Type = Type
        new.n1j = n1j 
        return new 


    def copy(self):
        return self.intbyCoreValue( self.Type, self.n1j  )
        # new = self.__new__( self.__class__ )
        # new.Type = self.Type
        # new.n1j = self.n1j 
        # return new 
    
    def getTN(self):
        return self.Type,self.n1j

    @staticmethod
    def _Num2List(val:int):
        r = []
        while val != 0:
            r.append( val % 4 ) 
            val //= 4
        return r
    
    @staticmethod
    def _List2Num(l):
        r = 0 
        for i, v in enumerate(l):
            r += v * (4**i) 
        return r

    @classmethod
    def _mulMap(cls,a,b):
        la, lb = cls._Num2List(a) , cls._Num2List(b) 
        lena, lenb = len(la), len(lb)
        L = max(lena,lenb) 
        la += [0]*(L-lena) 
        lb += [0]*(L-lenb)  
        P,F = 0, 0
        r = []
        for i in range(L):
            A = PauliGroupElement1(la[i])
            B = PauliGroupElement1(lb[i])
            t,n = (A*B).getTN() 
            r.append(t) 
            F += n 
        P = cls._List2Num(r) 
        F = F % 4
        return P,F 
    
    def __mul__(self,other,r=False):
        new = self.copy() 
        # if type(other) is type(self):
        if isinstance(other , self.__class__):
            if r:
                a,b = other.Type, self.Type
            else:
                a,b = self.Type, other.Type
            P,F = self._mulMap(a,b)
            new.Type = P 
            new.n1j = ( self.n1j + other.n1j + F ) % 4  
            return new 
        else: 
            if other == 1:
                pass 
            elif other == -1:
                new.n1j += 2
            elif other == 1j:
                new.n1j += 1
            elif other == -1j:
                new.n1j +=  3    
            else: 
                raise pauliOperatorError(f"illegal operation multiplex between [{self.__class__.__name__}] and {other}")
            new.n1j %= 4
            return new
        
    def __rmul__(self,other):
        return self.__mul__(other,r=True)

    def __pow__(self,n:int):
        # assert type(n) in (int,np.int_)
        assert not isinstance(n, numbers.Integral)
        new = self.copy() 
        if n < 0:
            assert False
        elif n == 0:
            return new 
        else: 
            for _ in range(n-1):
                new = new * self 
            return new 

    def __repr__(self):
        pList = self._Num2List(self.Type)
        OperName = ''.join([ ['I','X','Y','Z'][k] for k in pList])
        f = (['','i','-','-i'][self.n1j]).rjust(3, ' ')
        r = f"{f}{OperName}"
        return r 
    
    def _operatorHash(self) -> int:
        """hash of operator, without factor part

        Returns:
            int: hash value
        """        
        return self.Type
    
    def __hash__(self) -> int:
        return self._operatorHash() 
    
    def cleanFactor(self):
        self.n1j = 0 
    
    def getmatrix(self,nq:int|None=None):
        pList = self._Num2List(self.Type)
        if nq is None:
            nq = len(pList) 
        pList = pList + [0] * (nq-len(pList))  
        res = PauliGroupElement1(pList[-1]).getmatrix()
        for p in pList[:-1][::-1]:
            m = PauliGroupElement1(p).getmatrix()
            res = np.kron(res,m)
        return res * ((1j)**self.n1j)  


    



class pauliOperator(object):
    
    def __init__(self,elements):
        """_summary_

        Args:
            elements (tuple): (P,f) where P is Gn and f is a number
        """  
        self._data = {} 
        for e in elements:
            P,f = e  
            t,n = P.getTN()
            if t not in self._data:
                self._data[t] = (1j)**n * f 
            else:
                self._data[t] += (1j)**n * f 

    @classmethod
    def get0(cls):
        """
        return a empty container 
        """        
        return cls.intbyCoreValue( {} ) 
    
    @classmethod
    def get1(cls):
        """
        return a empty container 
        """        
        return cls.intbyCoreValue( {0:1} ) 


    def copy(self):
        new = self.__new__(self.__class__) 
        new._data = dict(self._data)
        return new 
    
    @classmethod 
    def intbyCoreValue(cls,data):
        new = object.__new__(cls)
        new._data = dict(data) 
        return new  

    def _add_on_Gn(self,P,f):
        Type, n1j = P.getTN() 
        if Type not in self._data:
            self._data[Type] = (1j**n1j) * f 
        else:
            self._data[Type] += (1j**n1j) * f 
        return self 

    def _mul_on_Gn(self,P,f,r=False):
        data = {} 
        Type,n1j = P.getTN() 
        for dType in self._data:
            if r:
                type2, type1 = dType, Type 
            else:
                type1, type2 = dType, Type 
            P1 = P.__class__.intbyCoreValue(Type=type1,n1j=0) 
            P2 = P.__class__.intbyCoreValue(Type=type2,n1j=0) 
            t,n = (P1*P2).getTN() 
            if t not in data:
                data[t] = self._data[dType] * f * (1j)** (n + n1j) 
            else:
                data[t] *= self._data[dType] * f * (1j)** (n + n1j) 
        self._data = data 
        return self 
    
    def __add__(self,other):
        new = self.copy() 
        for k in other._data:
            if k not in new._data:
                new._data[k] = other._data[k] 
            else:
                new._data[k] += other._data[k]
        return new.simplify()  
    
    def __sub__(self,other):
        return self + (-1)*other
    
    def __mul__(self,other,r=False):
        if isinstance(other, self.__class__ ):
            new = self.intbyCoreValue({0:0}) 
            for k in other._data:
                selfCopy = self.copy() 
                P = PauliGroupElementn.intbyCoreValue(Type=k,n1j=0)
                new = new + selfCopy._mul_on_Gn(P=P,f=other._data[k],r=r)  
        else:
            new = self.copy() 
            for k in new._data:
                new._data[k] *= other 
        return new.simplify() 
    
    def __rmul__(self,other):
        return self.__mul__(other=other,r=True) 
    
    def __pow__(self,n):
        new = self.copy() 
        if n < 0:
            assert False
        elif n == 0:
            new._data = {0:1}
        elif n == 1:
            return new 
        else:
            for _ in range(n-1):
                new = new * self 
        return new.simplify()  

    def __repr__(self):
        r = 'Pauli operator:\n'
        str_F_list = [] 
        str_P_list = []
        for k in self._data:
            plist = PauliGroupElementn._Num2List(k)
            OperName = ''.join([ ['I','X','Y','Z'][k] for k in plist])
            if len(OperName) == 0:OperName='I' 
            str_P_list.append( OperName )
            str_F_list.append( f"{self._data[k]}" )
        pLen = 0 
        for i in str_P_list:
            pLen = max(pLen,len(i)) 
        for i in range(len(str_P_list)):
            line = str_P_list[i].ljust(pLen, 'I') + f" : { str_F_list[i] }"
            r += f"  {line}\n"
        return r 
    
    def addConstant(self,val):
        if 0 not in self._data:
            self._data[0] = val 
        else:
            self._data[0] += val 
    
    def simplify(self):
        """One can call it when needed.
        Scan internal data to check if it can be simplified

        Returns:
            self: 
        """        
        zero = 10**-14
        keys = list(self._data.keys())
        for k in keys:
            if abs(self._data[k]) <= zero:
                del self._data[k] 
            elif abs( self._data[k].imag ) <= zero:
                self._data[k] = self._data[k].real
            else:
                pass
        return self 
    
    def exportPauliHamiltonian(self):
        # PauliHamiltonian()
        tmp = {} 
        for k in self._data:
            plist = PauliGroupElementn._Num2List(k) 
            tmp[k] = {'l':plist,'v':self._data[k]}
        N = 0 
        for k in tmp:
            N = max(N,len(tmp[k]['l'])) 
        h = PauliHamiltonian(nq=N) 
        for k in tmp:
            if k == 0:
                continue
            l = len(tmp[k]['l'])
            p = tmp[k]['l'] + [0] * (N-l)  
            h.setOneTerm( xi= tmp[k]['v'], p = p )
        if 0 in tmp:
            h.add_dH( tmp[0]['v'] )
        return h.simplify()
    
    def getmatrix(self,nq:int|None=None):
        tmp = {} 
        for k in self._data:
            plist = PauliGroupElementn._Num2List(k) 
            tmp[k] = {'l':plist,'v':self._data[k]}
        if nq is None:
            N = 0 
            for k in tmp:
                N = max(N,len(tmp[k]['l'])) 
        else:
            N = nq 
        con = np.zeros(shape=(2**N,2**N))
        for k in tmp:
            if k == 0:
                continue
            l = len(tmp[k]['l'])
            p = tmp[k]['l'] + [0] * (N-l)  
            con = con + PauliGroupElementn(elements= ( (p[i],i) for i in range(N) ) ).getmatrix(nq=N) * tmp[k]['v']
        con = con + np.eye(N=2**N) * tmp.get(0,0) 
        return con 

            

        # tmp = {} 
        # for k in self._data:
        #     plist = PauliGroupElementn._Num2List(k) 
        #     tmp[k] = {'l':plist,'v':self._data[k]}
        # N = 0 
        # for k in tmp:
        #     N = max(N,len(tmp[k]['l'])) 
        # h = PauliHamiltonian(nq=N) 
        # for k in tmp:
        #     if k == 0:
        #         continue
        #     l = len(tmp[k]['l'])
        #     p = tmp[k]['l'] + [0] * (N-l)  
        #     h.setOneTerm( xi= tmp[k]['v'], p = p )
        # if 0 in tmp:
        #     h.add_dH( tmp[0]['v'] )
        # return h.simplify()






