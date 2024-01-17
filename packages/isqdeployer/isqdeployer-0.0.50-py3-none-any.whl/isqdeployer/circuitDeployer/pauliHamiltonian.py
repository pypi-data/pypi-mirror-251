from __future__ import annotations
import numpy as np
from .abcDeployer import BaseDeployer
from ..utils.pauliHamiltonian import PauliHamiltonian
from ..circuit import isqInputArgument
from numbers import Real
import logging


class PauliDeployerError(Exception):pass

class Deployer(BaseDeployer):
    """
    target: isQ.Physics.pauliHam.isq


    """

    def _Preambles(self):
        return ["import isQLib.Physics.pauliHam;"]

    def expHt(self, h:PauliHamiltonian, t:Real|isqInputArgument, N:Real|isqInputArgument):
        NQ_Ham = h.getNq()
        NQ_deployer = self.getNq()
        if NQ_Ham != NQ_deployer: 
            raise PauliDeployerError(f"Num of Qubits in hamiltonian ({NQ_Ham}) != deployer ({NQ_deployer}) ")
        exist, varName = self.get_isqVarName_by_pyObject(h)
        varName_xi = varName + "_xi"
        varName_P = varName + "_P"
        if not exist:
            xiList = np.array(h.get_factor())
            PList = np.array(h.get_pauliOperators())
            self.circuit.defineArray_autoSet(varName=varName_xi, data=xiList)
            self.circuit.defineArray_autoSet(varName=varName_P, data=PList)
        varName_t = self.get_isqVarNameWithAppendIsQ(t)
        varName_N = self.get_isqVarNameWithAppendIsQ(N)
        varName_Q = "[" + ",".join([f"Q[{i}]" for i in self.qMap]) + "]"
        self.circuit.appendCode(
            f"deploy_expH_TS( {varName_xi} , {varName_P}, {varName_t}, {varName_Q}, {varName_N} ); "
        )
        return self 
    
    def gate4PauliMeasure(self,P):
        """_summary_

        Args:
            P (list): A list of integers to represent a pauli operator P. 
            To measure P directly on circuit, we need a (set of) conditional operator(s). This gate implement that.  

        Returns:
            self: 
        """        
        pTuple = tuple(P)
        exist, varName = self.get_isqVarName_by_pyObject(pTuple)
        varName_Q = self.getString_AllQubit()
        if not exist:
            self.defineArray_autoSet(varName=varName,data=P) 
        self.circuit.appendCode(
            f"deploy_PauliOperator_Measurement( {varName_Q}, {varName} ); "
        )
        return self 
    
    # def gate4PauliMeasureOnHamiltonian(self,h,i):
    #     r'''For a given Hamiltonian 
    #         :math:`H = \sum_i \xi_i P_i` 
    #     when we want to calculate \langle P_i \rangle, we need to deploy gate by `gate4PauliMeasure`. This sub automatically
    #     find the corresponding gate to deploy.   

    #     Args:
    #         h (pauli Hamiltonian): Hamiltonian object
    #         i (int): the i-th term in h
    #     '''
    #     pass 

    def ControlledPauliGate(self,P,controlID):
        """
        deploy a controlled-PauliGate

        Args:
            P (list): [int] represents a Pauli gate
            controlID (int): absolute qubit id on the circuit. The index in P must match qMap 
        """  
        cMap = self.circuit.getqMap()
        varName_Q = self.getString_AllQubit()
        varName_P = self.get_isqVarNameWithAppendIsQ(P)
        self.circuit.appendCode(
            f"deploy_CtrlPauliOperator( Q[{cMap[controlID]}], {varName_Q}, {varName_P}  ); "
        )
        return self 