from __future__ import annotations
from ..circuitDeployer.abcDeployer import BaseDeployer
from ..circuit import Circuit

class AnsatzError(Exception):pass 






class BaseAnsatz():

    def __init__(self,**kw):
        '''
        can be re-defined if needed
        '''

    def setTheta(self,theta:list):
        r"""before deploy gates onto circuit, one can reset theta by this function.

        Args:
            theta (list): element can be float or circuit.args

        Returns:
            _type_: _description_
        """        
        self._THETA = theta 
        return self 

    def getDeployerClass(self) -> BaseDeployer:
        """
        return a class (NOT a instance) of Deployer type. 
        This deployer has a method called "setAnsatz()" to deploy ansatz gates onto circuit  
        if circuit.lockedMap is used, before calling setAnsatz(), donot call `circuit._removeLockedMap()`

        Returns:
            Deployer: a deployer class (not object)
        """   
        if not hasattr(self,'_THETA'):
            raise AnsatzError('''theta is not set in ansatz, use method "setTheta(theta)" to set it.''')    
        class _depoler(BaseDeployer):
            def _Preambles(self):return []
            def setAnsatz(this):
                self.setAnsatz(this.circuit,self._THETA)  
        return _depoler 
    
    #-------------------------------------------------------
                
    def setAnsatz(self,circuit:Circuit,theta:list):
        '''
        for a given circuit object, define gates on it. 
        '''
        raise AnsatzError(f"method setAnsatz is not defined in class {self.__class__.__name__}")

