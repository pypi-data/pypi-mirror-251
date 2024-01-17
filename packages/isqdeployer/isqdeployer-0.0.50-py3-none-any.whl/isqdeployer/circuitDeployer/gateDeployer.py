import logging
from .abcDeployer import BaseDeployer



class BasicGateError(Exception):pass 

class Deployer(BaseDeployer):
    """
    realize basic gates in isQ


    """

    def _Preambles(self):
        return ["import std;"]
    
    def _singleGate(self,callerName,i):
        '''
        single-qubit gate without parameters
        '''
        self.circuit.appendCode(f"{callerName} (Q[{ self.qMap[i] }]);")
        return self 
    
    def _singleGateWith1Para(self,callerName,i,para):
        '''
        single-qubit gate with 1 parameter
        '''
        varName = self.get_isqVarNameWithAppendIsQ(para)
        callerName = callerName[0] + callerName[1].lower()
        self.circuit.appendCode(f"{callerName} (  {   varName   } ,  Q[{ self.qMap[i] }]);")
        return self 
    
    # def __getattr__(self, methodName ):
    #     methodName = methodName.upper()
    #     if methodName in ['X','Y','Z','H','S','T','X2P','X2M','Y2P','Y2M']:
    #         return lambda i:self._singleGate(methodName,i) 
    #     if methodName in ['RX','RY','RZ']:
    #         return lambda i,para:self._singleGateWith1Para(methodName,i,para)
    #     if methodName in ['CZ','CNOT']:
    #         def f(i,j):
    #             self.circuit.appendCode(f"{methodName} ( Q[{self.qMap[i]}] , Q[{self.qMap[j]}]);")
    #             return self 
    #         return f
    #     if methodName in ['U3']:
    #         def f( theta, phi, Lambda, i ):
    #             varName_theta = self.get_isqVarNameWithAppendIsQ( theta )
    #             varName_phi = self.get_isqVarNameWithAppendIsQ( phi )
    #             varName_lambda = self.get_isqVarNameWithAppendIsQ( Lambda )
    #             self.circuit.appendCode(f" U3 (  {varName_theta},{varName_phi},{varName_lambda},   Q[{ self.qMap[i] }]);")
    #             return self 
    #         return f 
    #     if methodName in ['TOFFOLI']:
    #         return lambda i,j,k:self.circuit.appendCode(f"Toffoli ( Q[{self.qMap[i]}] , Q[{self.qMap[j]}], Q[{self.qMap[k]}]  );")
    #     if methodName in ['GPHASE']:
    #         def f(theta):
    #             varName = self.get_isqVarNameWithAppendIsQ(theta)
    #             self.circuit.appendCode(f"GPhase (  {varName} );")
    #             return self 
    #         return f 
    #     # logging.error(f"undefined gate = [{methodName}]")
    #     raise BasicGateError(f"undefined gate = [{methodName}]")
    
    def X(self,i):
        return self._singleGate('X',i) 
    
    def Y(self,i):
        return self._singleGate('Y',i)
    
    def Z(self,i):
        return self._singleGate('Z',i)
    
    def H(self,i):
        return self._singleGate('H',i)
        
    def S(self,i):
        return self._singleGate('S',i)
    
    def T(self,i):
        return self._singleGate('T',i)
    
    def X2P(self,i):
        return self._singleGate('X2P',i)
    
    def X2M(self,i):
        return self._singleGate('X2M',i)
    
    def Y2P(self,i):
        return self._singleGate('Y2P',i)
    
    def Y2M(self,i):
        return self._singleGate('Y2M',i)
    
    def RX(self,i,para):
        return self._singleGateWith1Para('RX',i,para) 
    
    def Rx(self,i,para):
        return self.RX(i,para)

    def RY(self,i,para):
        return self._singleGateWith1Para('RY',i,para) 
    
    def Ry(self,i,para):
        return self.RY(i,para)

    def RZ(self,i,para):
        return self._singleGateWith1Para('RZ',i,para) 
    
    def Rz(self,i,para):
        return self.RZ(i,para)

    def CZ(self,i,j):
        self.circuit.appendCode(f"CZ ( Q[{self.qMap[i]}] , Q[{self.qMap[j]}]);")
        return self 
    
    def CNOT(self,i,j):
        self.circuit.appendCode(f"CNOT ( Q[{self.qMap[i]}] , Q[{self.qMap[j]}]);")
        return self 
    
    def U3(self,theta, phi, Lambda, i):
        varName_theta = self.get_isqVarNameWithAppendIsQ( theta )
        varName_phi = self.get_isqVarNameWithAppendIsQ( phi )
        varName_lambda = self.get_isqVarNameWithAppendIsQ( Lambda )
        self.circuit.appendCode(f" U3 (  {varName_theta},{varName_phi},{varName_lambda},   Q[{ self.qMap[i] }]);")
        return self 
    
    def u3(self,theta, phi, Lambda, i):
        return self.U3(theta, phi, Lambda, i)

    def TOFFOLI(self,i,j,k):
        self.circuit.appendCode(f"Toffoli ( Q[{self.qMap[i]}] , Q[{self.qMap[j]}], Q[{self.qMap[k]}]  );")
        return self 
    
    def GPHASE(self,theta):
        varName = self.get_isqVarNameWithAppendIsQ(theta)
        self.circuit.appendCode(f"GPhase (  {varName} );")
        return self 





    def test(self,i):
        return self._singleGate(i,'x')



