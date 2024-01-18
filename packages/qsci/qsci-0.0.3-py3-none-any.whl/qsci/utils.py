from collections import OrderedDict


#>>>>>>>>>>>>>>>>>>>>>>>>>>>> tmp >>>>>>>>>>>>>>>>>>>>>>>>
#--------------- import deployer--------
# import os,sys 
# sys.path.append(  os.path.join(os.environ['ALQ'],'Projects','isqdeployer')  )
# import isqdeployer as deployer 
import isqdeployer as isqdeployer
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
from isqdeployer.utils.cacheStore import CacheStore



class VariableTypeChecker():

    def __init__(self,ErrorException):
        self.EE = ErrorException
 
    def matchTypeRaiseError(self,srcVal,desType,funName=None):
        if not isinstance(srcVal,desType):
            funReminder = "" if funName is None else f"in @{funName}" 
            raise self.EE(f"variable type must be {desType}, this type is {type(srcVal)}. {funReminder}") 
        
    def batchVariableMatch1Type(self,srcVals,desType,funName=None):
        for v in srcVals:
            self.matchTypeRaiseError( srcVal = v,desType = desType, funName = funName )




class CacheDict(OrderedDict):
    """Store cache of simulation."""

    default_len = 100

    def __init__(self, *args, **kw):
        self.size_limit = kw.pop("maxlen", self.default_len)
        OrderedDict.__init__(self, *args, **kw)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)

