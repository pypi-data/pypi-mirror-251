import os 
import numpy as np 
from .import deployer
from .import SpinlessHamiltonian
from ...secondQuantization.qubitEncoding import JordanWignerEncoding


from isqdeployer.utils.pauliHamiltonian import PauliHamiltonian
from isqdeployer.ansatz.abcAnsatz import BaseAnsatz
from isqdeployer.backend.abcBackend import Backend
from isqdeployer.circuitDeployer.gateDeployer import Deployer as GateDeployer
from isqdeployer.circuitDeployer.pauliHamiltonian import Deployer as PauliDeployer



class RetardedGreenFunction():

    def __init__(self,backend:Backend,A:BaseAnsatz,H:SpinlessHamiltonian,Ntau:int,workDir=None):
        """
        For a given local fermion Hamiltonian, calculate the retarded Green's function G(t).
        The local Hamiltonian will use Jordan-Wigner encoding.

        Args:
            backend (Backend):
            A (BaseAnsatz): Ansatz object
            h (SpinlessHamiltonian): fermion Hamiltonian
            Ntau (int): _description_
            workDir (_type_, optional): _description_. Defaults to None.
        """   
        self.backend =  backend
        self.A = A     
        self.h = H.exportPauliOperator( JordanWignerEncoding() ).exportPauliHamiltonian() 
        self.Ntau = Ntau
        self.workDir = workDir 

    @staticmethod
    def _EPEP_PEPE_singleT(Ntau,t,simulator):
        res = simulator.runCircuit(F=[t],I=[Ntau])
        P0,P1 = 0,0
        for k in res:
            if k[-1] == '0':
                P0 += res[k]
            else:
                P1 += res[k]
        return 2 * ( P0 - P1  ) 
    
    def _get_P_chain(self,p,i):
        n = self.h.getNq()
        return [3] * i + [p] + [0] * ( n - i - 1) 


    # def EPEP_PEPE(self,Pi,i,Pj,j,Tlist):
    #     nq = self.h.getNq() # num of qubit used for Hamiltonian
    #     workDir = None if self.workDir is None else os.path.join(self.workDir,f"Pi{Pi}_i{i}_Pj{Pj}_j{j}")
    #     circuit = deployer.Circuit(backend=self.backend,nq=1+nq,isInputArg=True,workDir=workDir)
    #     gdpl = GateDeployer(circuit=circuit)
    #     pdpl = PauliDeployer(circuit=circuit,qMap=range(1,nq+1)) 
    #     circuit.setMeasurement([0])
    #     t = circuit.getInputArg('F',0)
    #     circuit._setqMap(qMap=list(range(1,nq+1)))
    #     ansatzdpl = self.A.getDeployerClass()(circuit=circuit) 
    #     # draw circuit
    #     gdpl.H(0).X(0) 
    #     ansatzdpl.setAnsatz()
    #     pdpl.ControlledPauliGate( P = self._get_P_chain(p=Pj,i=j), controlID = 0 ) 
    #     gdpl.X(0) 
    #     pdpl.expHt( h = self.h, t=t,N=self.Ntau) 
    #     pdpl.ControlledPauliGate( P = self._get_P_chain(p=Pi,i=i), controlID = 0 )
    #     gdpl.H(0)  
    #     results = circuit.runJob(paramList=[ {'F':[t]} for t in Tlist])
    #     RETURN = [] 
    #     for result in results:
    #         p0 = result.get('0',0)
    #         RETURN.append( 2*(2*p0-1) )
    #     return np.array(RETURN)
    def EPEP_PEPE(self,Pi,i,Pj,j,Tlist):
        nq = self.h.getNq() # num of qubit used for Hamiltonian
        workDir = None if self.workDir is None else os.path.join(self.workDir,f"Pi{Pi}_i{i}_Pj{Pj}_j{j}")
        circuit = deployer.Circuit(backend=self.backend,nq=1+nq,isInputArg=True,workDir=workDir)
        gdpl = GateDeployer(circuit=circuit)
        pdpl = PauliDeployer(circuit=circuit,qMap=range(1,nq+1)) 
        circuit.setMeasurement([0])
        t = circuit.getInputArg('F',0)
        circuit._lockMap(lockMap=list(range(1,nq+1)))
        ansatzdpl = self.A.getDeployerClass()(circuit=circuit) 
        gdpl.H(0)#.X(0) 
        ansatzdpl.setAnsatz()
        pdpl.ControlledPauliGate( P = self._get_P_chain(p=Pj,i=j), controlID = 0 ) 
        gdpl.X(0) 
        pdpl.expHt( h = self.h, t=t,N=self.Ntau) 
        pdpl.ControlledPauliGate( P = self._get_P_chain(p=Pi,i=i), controlID = 0 )
        gdpl.H(0)  
        results = circuit.runJob(paramList=[ {'F':[t]} for t in Tlist])
        RETURN = [] 
        for result in results:
            p0 = result.get('0',0)
            RETURN.append( 2*(2*p0-1) )
        return np.array(RETURN)

    def _GR1(self,i,j,Tlist):
        return self.EPEP_PEPE(Pi=1,i=i,Pj=2,j=j,Tlist=Tlist) 
    
    def _GR2(self,i,j,Tlist):
        return self.EPEP_PEPE(Pi=2,i=i,Pj=1,j=j,Tlist=Tlist) 
    
    def _GI1(self,i,j,Tlist):
        return self.EPEP_PEPE(Pi=1,i=i,Pj=1,j=j,Tlist=Tlist) 
    
    def _GI2(self,i,j,Tlist):
        return self.EPEP_PEPE(Pi=2,i=i,Pj=2,j=j,Tlist=Tlist) 
    
    def GR(self,i,j,Tlist):
        f = self._GR1(i,j,Tlist) 
        s = self._GR2(i,j,Tlist) 
        return ( f - s ) * (-1)**(i+j) / 4

    def GI(self,i,j,Tlist):
        f = self._GI1(i,j,Tlist) 
        s = self._GI2(i,j,Tlist) 
        return - ( f + s ) * (-1)**(i+j) / 4 
    
    def G(self,i,j,Tlist):
        return self.GR(i,j,Tlist) + 1j* self.GI(i,j,Tlist) 
    
    def etaGF(self,i,j,Tlist,eta):
        G = self.G(i,j,Tlist)
        return G*np.exp(-eta*Tlist)