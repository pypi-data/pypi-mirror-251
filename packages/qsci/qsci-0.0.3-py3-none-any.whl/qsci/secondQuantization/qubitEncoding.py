from abc import ABC,abstractmethod
from ..pauliOperator import pauliOperator,PauliGroupElementn

class EncodingError(Exception):pass 


class FermionEncoding(ABC):

    @abstractmethod
    def c(i):
        raise EncodingError("c not defined")
    
    @abstractmethod
    def cd(i):
        '''return PauliOperator'''

    @staticmethod
    def _pauliOperator(k,i):
        p = PauliGroupElementn(((k,i),))
        return pauliOperator(((p,1),)) 
    
    @classmethod
    def sigma_pm(cls,i,pm):
        """
          1/2 * (X +- i * Y)

        Args:
            i (int): site index
            pm (str): '+' or '-'

        Returns:
            _type_: _description_
        """   
        x = cls._pauliOperator(1,i) 
        y = cls._pauliOperator(2,i)
        if pm == '+':
            return 0.5*(x+1j*y)
        elif pm == '-':
            return 0.5*(x-1j*y)
        else:
            raise EncodingError(f"pm must in ['+','-'], but the input is {pm}")  

    @classmethod 
    def chainZ(cls,i:int,j:int) -> pauliOperator:
        """ Z_{i} Z_{i+1} ... Z_{j-1}

        Args:
            i (int): site index
            j (int): site index

        Returns:
            pauliOperator: _description_
        """    
        zList = [ (3,a) for a in range(i,j) ]    
        zGn = PauliGroupElementn( zList )
        return pauliOperator(((zGn,1),))
    
    @classmethod
    def get0(cls):
        return pauliOperator.get0( )
    
    @classmethod
    def get1(cls):
        return pauliOperator.get1( )




class JordanWignerEncoding(FermionEncoding):

    @classmethod
    def c(cls,i):
        sigma_m = cls.sigma_pm(i,'-')
        Z = cls.chainZ(0,i)
        return (-1)**i * sigma_m * Z
    
    @classmethod
    def cd(cls,i):
        sigma_p = cls.sigma_pm(i,'+')
        Z = cls.chainZ(0,i)
        return (-1)**i * sigma_p * Z





