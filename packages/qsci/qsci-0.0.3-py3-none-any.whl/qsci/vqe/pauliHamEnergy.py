from __future__ import annotations
import os 
import logging
from ..utils import isqdeployer

class vqeEnergyError(Exception):pass

# isqdeployer.utils.PauliHamiltonian

class PauliHamEnergy():

    def __init__(self,
                 h:isqdeployer.utils.PauliHamiltonian, 
                 az: isqdeployer.ansatz.BaseAnsatz,
                 backend=None, 
                 workDir = None, 
                 qMap=None, 
                ):
        self.h = h 
        self.az = az
        self.backend = backend
        self.workDir = workDir 
        self.qMap = qMap

    def _calculateEnergyByPauliMeasurement_eachTerm(self,theta:list[float],i:int):
        r""" for :math:`\langle H\rangle>=\sum_i \xi_i \langle P_i\rangle>`, calculate :math:`\langle P_i\rangle>`

        Args:
            theta (list[float]): _description_
            i (int): _description_
        """    
        #--------------------------------------
        th = {1:"st",2:"nd",3:"rd"}.get(i+1,"th")
        logging.debug(f"calculate the {i+1}-{th} term of H")    
        #--------------------------------------
        nq = self.h.getNq()
        xi = self.h.get_factor() 
        pL = self.h.get_pauliOperators() 
        if self.workDir is not None:
            cirWorkDir = os.path.join( self.workDir, f"{i}of{len(xi)}_Energy" )
        else:
            cirWorkDir = None
        circuit = isqdeployer.Circuit(nq=nq,isInputArg=True,workDir=cirWorkDir,backend=self.backend,qMap=self.qMap) 
        circuit.set_pauli_measurement(pL[i])
        thetaArgs = [circuit.getInputArg('F',k) for k in range(len(theta))]
        self.az.setTheta(thetaArgs) 
        dplClass = self.az.getDeployerClass() 
        dpl_G = dplClass(circuit=circuit) 
        dpl_G.setAnsatz() 
        p_dpl = isqdeployer.circuitDeployer.pauliHamiltonian.Deployer(circuit=circuit)
        p_dpl.gate4PauliMeasure(pL[i]) 
        jres = circuit.runJob(paramList=[{'F': list(theta) }])[0] 
        logging.debug(f"circuit job output: {jres}")
        result = 0
        for res_index, probs in jres.items():
            parity = (-1) ** (res_index.count("1") % 2)
            result += parity * probs
        return result
    
    def _calculateEnergyByHadamardTest_eachTerm(self,theta:list[float],i:int):
        r""" for :math:`\langle H\rangle>=\sum_i \xi_i \langle P_i\rangle>`, calculate :math:`\langle P_i\rangle>`
        Use Hadamard test

        Args:
            theta (list[float]): _description_
            i (int): _description_
        """    
        #--------------------------------------
        th = {1:"st",2:"nd",3:"rd"}.get(i+1,"th")
        logging.debug(f"calculate the {i+1}-{th} term of H")    
        #--------------------------------------
        nq = self.h.getNq()
        xi = self.h.get_factor() 
        pL = self.h.get_pauliOperators() 
        if self.workDir is not None:
            cirWorkDir = os.path.join( self.workDir, f"{i}of{len(xi)}_Energy" )
        else:
            cirWorkDir = None
        circuit = isqdeployer.Circuit(nq=nq+1,isInputArg=True,workDir=cirWorkDir,backend=self.backend,qMap=self.qMap) 
        circuit.setMeasurement([0])
        dpl = isqdeployer.circuitDeployer.GateDeployer(circuit=circuit)
        p_dpl = isqdeployer.circuitDeployer.pauliHamiltonian.Deployer(circuit=circuit,qMap=list(range(1,1+nq)))
        thetaArgs = [circuit.getInputArg('F',k) for k in range(len(theta))]
        circuit._lockMap(lockMap=list(range(1,1+nq))) 
        self.az.setTheta( thetaArgs ) 
        dplClass = self.az.getDeployerClass() 
        dpl_G = dplClass(circuit=circuit) 
        dpl.H(0)
        dpl_G.setAnsatz() 
        p_dpl.ControlledPauliGate(pL[i],0)
        dpl.H(0)
        jres = circuit.runJob(paramList=[{'F': list(theta) }])[0] 
        p0 = jres.get('0',0)
        return 2*p0 - 1 



    def calculateEnergy(self,theta:list[float],method:str|None=None):
        r""" 
            The size of circuit would be the same as H. An additional set of gates are needed for Pauli measurement. 
        Args:
            theta (list[float]): parameters in ansatz
            method (str | None, optional): "pauli"/"htest". Defaults to None.

        """   
        sub = {
            "pauli":self._calculateEnergyByPauliMeasurement_eachTerm,
            "htest":self._calculateEnergyByHadamardTest_eachTerm
        }  
        if method is None:
            method = "pauli"
        if method not in sub:
            raise vqeEnergyError(f'''no method name "{method}"''')  
        else:
            calc = sub[method.lower()] 
        xi = self.h.get_factor() 
        res = 0 
        for i in range(len(xi)):
            mean_P = calc(theta,i) 
            res += xi[i] * mean_P
        res += self.h.getdH() 
        return res  





    

