from __future__ import annotations
from abc import abstractmethod, ABC
import logging
import numpy as np



class UnknownTypeError(Exception):pass 

class DeployerError(Exception):pass 

class BaseDeployer(ABC):
    """
    realize operation on a circuit
    """

    def __init__(self, circuit, qMap:list|None = None):
        """
        qMap[i] represent the index of qubit on Circuit
        """
        self.circuit = circuit
        #----->>> handle circuit internal lockedMap >>>------
        #   gate --(qMap)--(lockMap)--> circuit --(cMap)--> harware
        cqMap = self.circuit.getqMap()
        if circuit._hasLockedMap():
            lockedMap = circuit._getLockedMap() 
            if qMap is None:
                self.qMap = [ cqMap[i] for i in lockedMap ]
            else:
                self.qMap = [ cqMap[lockedMap[i]] for i in qMap]
        else:
            self.qMap = cqMap if qMap is None else [ cqMap[i] for i in qMap]
        # --------
        self._autoSetPreambles()
        self.ID, self.STORE_ON_CIRCUIT = self.circuit.registDeployer()

    @abstractmethod
    def _Preambles(self) -> list:
        """
        example: "import demoLib.isQ.Physics.pauliHam;"
        """

    def _autoSetPreambles(self):
        for preamble in self._Preambles():
            self.circuit.appendPreambleIfNotExist(preamble)
        return self

    def get_isqVarName_by_pyObject(self, Obj):
        """
        For a given Python object Obj, according to its hash value to check if it is recorded in varName-cache.
        If it exists, return [True,varName]
        If not exist, make a record and return [False,varName]
        NOTE: this function do not append code into isQ.
        """
        dictKey = "varNameCache"
        if dictKey not in self.STORE_ON_CIRCUIT:
            self.STORE_ON_CIRCUIT[dictKey] = {}
        p = self.STORE_ON_CIRCUIT[dictKey]
        if type(Obj) in [list,np.ndarray]:
            key = hash(tuple(Obj)) 
        elif Obj.__hash__ is None:
            raise DeployerError(f"Object is not hashable: {Obj}")
        else:
            key = hash(Obj) 
         
        if key not in p:
            exist = False
            varName = "var_" + str(self.ID) + "_" + str(len(p))
            p[key] = varName
        else:
            exist = True
        return exist, p[key]

    def get_isqVarNameWithAppendIsQ(self, Obj):
        """
        For some types, we can do more than [get_isqVarName_by_pyObject].
        This function first check varName-cache, then automatically insert isQ code for defining variable
        """
        if type(Obj) is self.circuit._getInternalClass("inputArgumentClass"):
            return Obj.get_paraName_in_isq()
        exist, varName = self.get_isqVarName_by_pyObject(Obj=Obj)
        if not exist:
            if type(Obj) in [int, np.int_]:
                self.circuit.defineVariable(FI="I", varName=varName, value=Obj)
            elif type(Obj) in [float, np.float_]:
                self.circuit.defineVariable(FI="F", varName=varName, value=Obj)
            elif type(Obj) in [list, np.ndarray]:
                self.circuit.defineArray_autoSet(varName=varName, data=Obj)
            else:
                raise UnknownTypeError(f" type {type(Obj)}  is not supported now")
                # logging.error(
                #     f"unknown type = [{type(Obj)}] in get_isqVarNameWithAppendIsQ"
                # )
        return varName
    
    def defineArray_autoSet(self,varName,data):
        self.circuit.defineArray_autoSet(varName=varName, data=data) 
        return self 
    
    def getString_AllQubit(self):
        return "[" + ",".join([f"Q[{i}]" for i in self.qMap]) + "]"
    
    def getNq(self):
        """get num of qubits in this block, len(qMap)
        """        
        return len(self.qMap) 




