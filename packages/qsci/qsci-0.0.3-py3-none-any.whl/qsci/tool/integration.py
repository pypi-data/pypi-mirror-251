import numpy as np 
import logging 

class GaussLegendreIntegration():
    """generate sampling points for integration 

    """    
    # integration by GaussLegendre method 
    #
    # [init]
    # 
    # [fun] getzw(n,z1,z2)
    #       return x,w 
    #
    # [fun] itgFunc(n,z1,z2,func)
    #
    # [fun] itgFunCache(n,z1,z2,funCache,expr) 

    def __init__(self):
        self.cache = {} 

    @staticmethod
    def zerosOfLegendre(N):
        """find zeros of legendre polynomial P_N(x)

        Args:
            N (int): order N

        Returns:
            list: zeros
        """        
        return np.polynomial.legendre.legroots( [0]*N+[1] )
    
    @staticmethod
    def legendreP(N,x):
        return np.polynomial.legendre.Legendre.basis(N)(x)
    
    def directGenerate_xw0(self,n):
        zeros = self.zerosOfLegendre(n)
        W=2.0*(1.0-zeros**2.0)/( self.legendreP(n+1,zeros) *(n+1))**2.0
        return zeros,W
    
    def get_cache_xw0(self,n):
        if n not in self.cache:
            self.cache[n] = self.directGenerate_xw0(n)
        return self.cache[n] 
    
    def getzw(self,n,z1,z2):
        """majorly use this function 

        Args:
            n (int): number of points
            z1 (float/complex): start point
            z2 (float/complex): end point

        Returns:
            (x,w): list of x and w 
        """        
        x0,w0 = self.get_cache_xw0(n) 
        l = np.abs(z2-z1)
        x = x0 * l/2 + (z1+z2)/2
        w = w0 * l / 2  
        return x,w 

    def itgFunc(self,n,z1,z2,func):
        x,w = self.getzw(n,z1,z2)
        r = 0 
        for i in range(len(x)):
            r += func(x[i]) * w[i] 
        return r

    def itgFunCache(self,n,z1,z2,funCache,expr):
        # expr is a function f=f(x,c) where c is the cache value
        if len(funCache) != n:
            logging.error('length of function-cache does not match');return  
        x,w = self.getzw(n,z1,z2)
        r = 0 
        for i in range(len(x)):
            r += expr(x[i],funCache[i]) * w[i] 
        return r