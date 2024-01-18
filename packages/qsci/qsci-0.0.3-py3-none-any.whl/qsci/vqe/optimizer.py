from __future__ import annotations
import os 
import logging
from .pauliHamEnergy import PauliHamEnergy
from ..utils import CacheDict
from ..utils import CacheStore
import numpy as np 
from collections import Iterable
# from isqdeployer.utils.PauliHamiltonian
from isqdeployer.utils import PauliHamiltonian
from isqdeployer.backend.abcBackend import Backend
from isqdeployer.ansatz.abcAnsatz import BaseAnsatz
import shutil
import json 
import matplotlib.pyplot as plt
import matplotlib
from rich.console import Console
import time 



class _Timer():

    def __init__(self):
        self.t = 0
    
    def add(self,dt):
        self.t += dt 
        return self 

    def start(self):
        self.t_start = time.time() 
        return self 
    
    def stop(self):
        dt = time.time() - self.t_start 
        return self.add(dt)
    
    def __repr__(self) -> str:
        ty_res = time.gmtime(self.t)
        res = time.strftime("(%H h:%M m:%S s)",ty_res)
        return res
        # h = self.t // 3600
        # m = (self.t - h*3600)//60
        # s = (self.t - h*3600 - 60 * m )
        # r = '' 
        # if h >0:
        #     r+= f"{h} hour(s)"
        # if m>0:
        #     r+= f"{m} minute(s)"
        # if s>0:
        #     r+= f"{s} second(s)"
        # return r 

class Result():
    def __init__(self,**kw):
        self.kw = kw 


class Optimizer():

    DEFAULT_dx = 0.01
    DEFAULT_gtol = 0.1
    DEFAULT_maxIter = 100


    def __init__(self,
                 ham:PauliHamiltonian, 
                 az:BaseAnsatz , 
                 backend:Backend , 
                 qMap:list|None = None,
                 config:dict = {}, 
                 workDir:str|None = None ,
                 isMin = True,
                 **kw
                 ):
        self.phe = PauliHamEnergy(h=ham,az=az,backend=backend,workDir=workDir,qMap=qMap)
        self.yCache = CacheDict(maxlen=2000)
        self.gCache = CacheDict(maxlen=2000)
        self._isMin = isMin
        self._direction = 1 if isMin else -1 
        self.config = dict(config) 
        if workDir is not None:
            self.logDir = os.path.join( workDir, "optimize_log" )
            if os.path.exists(self.logDir):
                shutil.rmtree(self.logDir) 
            os.makedirs(self.logDir)
        else:
            self.logDir = None
        self._calcTime = _Timer()

    def getParam(self,key:str) -> float|complex|list|None:
        r"""return internal parameter if there is any

        Args:
            key (str): parameter name 
        """        
        if key in self.config:
            return self.config[key]
        else:
            keyName = "DEFAULT_" + key 
            if hasattr(self,keyName):
                return getattr(self,keyName)
            else:
                return None
        

    def _recordLog(self,sectionName,dataDict):
        if self.logDir is None:return 
        filePath = os.path.join( self.logDir, sectionName )
        with open(filePath,'w') as f:
            f.write(json.dumps(dataDict, indent=4))



    def _getXKey(self,x):
        return tuple(x) 

    def _gety(self,x):
        key = self._getXKey(x) 
        if key not in self.yCache:
            e = self.phe.calculateEnergy(theta = x)
            self.yCache[key] = e  
        return self.yCache[key] 
    
    def _getg(self,x):
        key = self._getXKey(x) 
        if key not in self.gCache:
            dx = self.config.get( 'dx', None ) 
            if dx is None:
                dx = [ self.DEFAULT_dx ] * len(x) 
            else:
                if not isinstance(dx, Iterable):
                    dx = [ dx ] * len(x) 
            g = [] 
            for i in range(len(x)):
                DX = np.array([0.0]*len(x))
                DX[i] = dx[i]
                x2 = np.array(x) + DX
                gi = ( self._gety(x2) - self._gety(x) ) / dx[i] 
                g.append( gi )
            self.gCache[key] = np.array(g) 
        return self.gCache[key] 
    
    # def _gety_withdirection(self,x):
    #     if self.isMin:
    #         return self._gety(x) 
    #     else:
    #         return -self._gety(x)
        
    # def _getg_withdirection(self,x):
    #     if self.isMin:
    #         return self._getg(x) 
    #     else:
    #         return -self._getg(x)
    






class GradientDescent_Base(Optimizer):


    _DEFAULT_gamma = 0.1

    def minimize(self,x0):
        maxIter = self.config.get('maxIter',self.DEFAULT_maxIter)
        c = 0 
        x1 = np.array(x0)
        while True:
            c += 1
            x2,g0 = self._moveStep( x = x1 )
            self._recordLog(sectionName="step"+f"{c}".rjust(3,'0')+".txt",dataDict = {
                "x0":list(x1),
                "x1":list(x2),
                "g0":list(g0),
                "y0":self._gety(x1),
            })
            logging.info("optimize step " + (f"{c}").rjust(3, ' ') + f" : energy={self._gety(x1)}")
            if self.isConverged(x1=x1,x2=x2,y1=self._gety(x1),y2=self._gety(x2),g=g0):
                return {
                    "theta": x2,
                    "Energy":self._gety(x2)
                }
            if c == maxIter:
                logging.error(f"cannot converge within {maxIter} steps, stop")
                return 
            x1 = x2 
    
    def _moveStep(self,x0,gamma=None):
        self._calcTime.start()
        if gamma is None:
            gamma = self.config.get('gamma', self._DEFAULT_gamma )
        logging.debug(f"start moving step (gamma= {gamma})")
        g = self._getg(x=x0) 
        logging.debug(f"g = {g}")
        xp = np.array(x0) - gamma * g * self._direction 
        self._calcTime.stop()
        logging.debug(f"new position: {xp}")
        return xp, g 
    
    def _moveSteps(self,x0,Nstep:int,gamma=None):
        x_start = x0 
        for _ in range(Nstep):
            xp,g = self._moveStep(x_start,gamma=gamma) 
            x_start = xp  

    
    def isConverged(self,x1,x2,y1,y2,g):
        gtol = self.config.get('gtol',None)
        if gtol is None:
            pass 





class GradientDescent_interactive(GradientDescent_Base):

    def __init__(self,x0,**kw):
        super().__init__(**kw) 
        if 'workDir' not in kw:
            raise Exception("must set 'workDir' in __init__")
        self.workDir = kw['workDir']
        self.logLocalStore = os.path.join( self.workDir, "localstore_interactive" )
        self.localStore = CacheStore( filePath = self.logLocalStore )
        self.localStore.clean() 
        self.localStore.setdl( key='x0', val= {"x":list(x0)}  )
        self.console = Console(height=5)

    def _move(self,gamma=None):
        count = self.localStore.get("count",0) 
        pointData = self.localStore.getdl(key=f"x{count}")  
        x_s = np.array(pointData['x'])
        x_e,g = self._moveStep(x0= x_s ,gamma=gamma)
        pointData['g'] = list(g) 
        pointData['gamma'] = gamma 
        pointData['y'] = self._gety(x=x_s)
        self.localStore.setdl(key=f"x{count}",val=pointData) 
        self.localStore.setdl(key=f"x{count+1}",val={'x':list(x_e)})
        self.localStore.set("count",count+1) 
        #------------- report -------------
        y = self._gety(x=x_s)
        reportStr = f"[bold]step {count}:[/bold] energy = {y}  "
        if count > 0:
            y_last = self.localStore.getdl(key=f"x{count-1}")['y'] 
            if y_last > y:
                arrow = "[bold green]⬇[/]"
            elif y_last < y:
                arrow = "[bold red]⬆[/]"
            else:
                arrow = ''
        else:
            arrow = ''
        reportStr += arrow
        # style = "bold white on blue"
        self.console.print(reportStr)
        
    
    def fixStepOptimize(self,nStep:int,gamma:float|None=None):
        for _ in range(nStep):
            self._move(gamma=gamma) 

    def showHist(self,ax:matplotlib.axes.Axes|None=None):
        """ show data of each step in the iteration 

        Args:
            ax (matplotlib.axes.Axes | None, optional): _description_. Defaults to None.
        """    
        if ax is None:
            ax = plt.axes()
        N = self.localStore.get('count') 
        if N == 0 :
            logging.warn("localstore data is empty")
            return
        kl = [ f"x{i}" for i in range(N)]
        data = self.localStore.batchGetdl(keyList=kl) 
        ax.plot(range(N),[d['y'] for d in data],'--',color='C10') 
        maxColorNum = 9 # must <= 9
        gammaColor = {}
        gammaDots = [] 
        for i in range(N):
            gamma = data[i]['gamma']
            if gamma in gammaColor:
                idx = gammaColor[gamma] 
            else:
                l = len(gammaColor) 
                if l < maxColorNum-1:
                    idx = gammaColor[gamma] = l
                    gammaDots.append({'x':[],'y':[],'label':"$\gamma={:1.6f}$".format(gamma)})
                else:
                    idx = maxColorNum - 1
                    gammaDots.append({'x':[],'y':[],'label':"$\gamma=others$"})
            gammaDots[idx]['x'].append(i)
            gammaDots[idx]['y'].append(data[i]['y'])
        for i in range(len(gammaDots)):
            d = gammaDots[i]
            ax.plot( d['x'],d['y'],'o', label=d['label'], color="C"+str(i) )
        ax.set_xlabel('iteration step') 
        ax.set_ylabel("Energy (price function)")
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
        ax.legend()
        ax.set_title(f"Cumulative elapsed: {self._calcTime}")






         
