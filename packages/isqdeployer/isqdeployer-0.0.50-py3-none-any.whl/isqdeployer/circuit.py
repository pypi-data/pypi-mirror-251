from __future__ import annotations
import os
import tempfile
import logging
import numpy as np 
import json
from .isQmaker import isQ_maker
from .backend.numpy_simulator import Backend as DefaultSimulator
from .circuitDeployer.gateDeployer import Deployer as GateDeployer
from .utils.cacheStore import CacheStore as CacheStore
from .intermediateRepresentation import IR_based_on_QCIS as IR 
from .utils.fasthash import fasthash
 
import typing
try:
    import qiskit 
    QiskitCircuit = qiskit.QuantumCircuit
except:
    QiskitCircuit = typing.Any


class CircuitError(Exception):
    """"""


class isqInputArgument:
    @staticmethod
    def getParaName():
        return "intPara", "floPara"

    def __init__(self, FI: str, id: int):
        """
        FI = 'F' for float (double), 'I' for int
        """
        self.FI = FI
        self.id = id

    def get_paraName_in_isq(self):
        # paraNames = self.getParaName()

        return self.getParaName()[{"F": 1, "I": 0}[self.FI]] + f"[{self.id}]"


class Circuit:

    def __init__(self, nq: int, isInputArg=False, workDir=None, backend=None,qMap=None):
        """Essentially this class is used to maintain a pice of isQ code. No direct operations can be done on it.
        To interact with circuit, one must use a circuitDeployer

        Args:
            nq (int): number of qubit in total
            isInputArg (bool, optional): use isq parameters or not. Defaults to False.
            workDir (_type_, optional): working space. Defaults to None.
            backend (_type_, optional):  Defaults to None.
            qMap (_type_, optional): qMap, used for hardware mapping
        """        
        self.nq = nq
        self._isInputArg = isInputArg  # input arguments
        #---------------- set backend ----------------------
        if backend is None:
            logging.warn("No input backend, use default simulator")
            backend = DefaultSimulator() 
        self._backend = backend
        self._backend._setCircuit(self)
        #---------------- qMap -----------------------------
        if qMap is None:
            self.qMap = list(range(self.nq))
        else:
            self.qMap = list(qMap) 
        #---------------- lockMap --------------------------
        self._islocked = False 
        self._lockedMap = None
        #---------------- cache data  ----------------------
        self._PREAMBLES_STORE = []
        self._CODE_VARIABLE_DEFINITION = []
        self._CODE_SUBROUTINE_DEFINITION = []
        self._CODE_PROGRAM_MAIN_BODY = []
        self._CODE_MEARSUREMENT = []
        self._DEPLOYER_STORE = []
        self._cls = {
            "inputArgumentClass": isqInputArgument,
            "isQmaker": isQ_maker,
        }
        if workDir is None:
            self._tmpDirObj = tempfile.TemporaryDirectory()
            self._workDir = self._tmpDirObj.name
            self._isDelNeeded = True
        else:
            self._workDir = workDir
            self._isDelNeeded = False
            if not os.path.exists(self._workDir):
                os.makedirs(self._workDir)
        #------------------------------- circuit dependent local-store ----------------------------
        self._localstore = CacheStore( filePath = os.path.join(self._workDir, "results.json") ) 
        #----------------------------------- IR ---------------------------------------------------
        self._ir = IR( 
            isqPath = os.path.join(self._workDir, "resource.isq"), 
            cacheStore = self._localstore,
            )
        #----------------- contains a default deplyer for simply gate -----------------------------
        self._defaultGate = GateDeployer(circuit=self) 

    def _getInternalClass(self,className):
        return self._cls[className]
    
    def getWorkDir(self):
        return self._workDir

    def __del__(self):
        if hasattr(self, "isDelNeeded") and self._isDelNeeded:
            self._tmpDirObj.cleanup()

    def make_isq_resource(self):
        """
        1. write isq file
        2. compile to get .so file
        """
        isqCode = self._makeCode()
        new_isqhash = fasthash(isqCode)
        isqFile = os.path.join(self._workDir, "resource.isq")
        if os.path.exists(isqFile):
            old_isqHash = self._localstore.get(key="CIRCUIT_isqcodehash",default=None)
            if new_isqhash == old_isqHash:
                self.isCreateIsQNeeded = False
            else:
                self.isCreateIsQNeeded = True
        else:
            self.isCreateIsQNeeded = True
        if self.isCreateIsQNeeded:
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #    put lib dir (isq lib for compiling)
            # -----------------------------------------------------
            LIB_ENVIRON = os.environ.get("LIB_ENVIRON", None)
            if LIB_ENVIRON is None:
                src_isqLib = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "isQ"
                )
            else:
                LIB_ENVIRON = json.loads(LIB_ENVIRON)
                src_isqLib = LIB_ENVIRON["ISQ"]
            dst_isqlib = os.path.join(self._workDir, "isQLib")
            try:
                os.remove(dst_isqlib)
            except:
                pass
            os.symlink(src=src_isqLib, dst=dst_isqlib)
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            with open(isqFile, "w") as f:
                f.write(isqCode)
            self._localstore.clean() 
            self._localstore.set("CIRCUIT_isqcodehash",new_isqhash)
            self._localstore.set("IR_needupdate",True)

    

    def getInputArg(self, FI: str, id: int):
        """
        FI = 'F' or 'I'
        get the <id>-th input argument
        """
        if self._isInputArg:
            return isqInputArgument(FI, id)
        else:
            logging.error(
                "circuit not support input argument, consider setting isInputArg=True"
            )

    def setMeasurement(self, qList):
        """set measurement on qubits

        Args:
            qList (list): int number represent the index of qbuit that will be measured.
        """
        self._CODE_MEARSUREMENT += qList
        # for qi in qList:
        #     if qi in self._CODE_MEARSUREMENT:
        #         logging.error(f"measurement on qubit {qi} more than once.")
        #     else:
        #         self._CODE_MEARSUREMENT.append(qi)
        # self._CODE_MEARSUREMENT.sort()
        #

    def getMeasurementList(self):
        return list(self._CODE_MEARSUREMENT)

    def set_pauli_measurement(self, P, qMap:list | None = None):
        """Pauli Measurement."""
        # self._CODE_MEARSUREMENT = []
        if qMap is None:
            qMap = list(range(self.nq))
        qList = []
        for idx, pauli in enumerate(P):
            if pauli == 0:
                continue
            elif pauli in [1, 2, 3]:
                qList.append( qMap[idx] )
            else:
                raise ValueError("Invalid Pauli.")
        self.setMeasurement(qList=qList)

    def isInputParameter(self):
        return self._isInputArg

    def getQN(self):
        return self.nq

    # def get_isQ_maker(self):
    #     return self._cls['isQmaker']

    def defineVariable(self, FI, varName, value):
        Type = {"F": "double", "I": "int"}[FI]
        self._CODE_VARIABLE_DEFINITION.append(f"{Type} {varName} = {value};")
        return self

    def defineArray_autoSet(self, varName, data):
        self._CODE_VARIABLE_DEFINITION.append(
            isQ_maker.autoSetArray(varName=varName, data=data)
        )
        return self

    def defineSubroutine(self, isQcode):
        self._CODE_SUBROUTINE_DEFINITION.append(isQcode)

    def registDeployer(self):
        self._DEPLOYER_STORE.append({})
        rid = len(self._DEPLOYER_STORE) - 1
        return rid, self._DEPLOYER_STORE[rid]

    def appendPreambleIfNotExist(self, preamble):
        if preamble not in self._PREAMBLES_STORE:
            self._PREAMBLES_STORE.append(preamble)

    def appendCode(self, codeBlock):
        self._CODE_PROGRAM_MAIN_BODY.append(codeBlock)
        return self

    def _makeCode(self):
        preamble = "\n".join(self._PREAMBLES_STORE)
        varDef = "\n".join(self._CODE_VARIABLE_DEFINITION)
        defSubroutine = "\n".join(self._CODE_SUBROUTINE_DEFINITION)
        body = "\n".join(self._CODE_PROGRAM_MAIN_BODY)
        measure = "\n".join([f"M ( Q[{self.qMap[q]}] );" for q in self._CODE_MEARSUREMENT])
        inputArgStr = (
            " int {0} [], double {1} []".format(*isqInputArgument.getParaName())
            if self._isInputArg
            else ""
        )

        

        code = (
            f"{preamble} \n"
            f"{defSubroutine} \n"
            f"qbit Q[{ max(np.array(self.qMap))+1 }];\n"
            f"procedure main( {inputArgStr} ) {{\n"
            f"// ------ define variables --------\n"
            f"{varDef}\n"
            "// ------ statements -----------\n"
            f"{body}\n"
            "// ------ measurement ------------\n"
            f"{measure}\n"
            "}"
        )

        return code

    @staticmethod
    def _getParaKey(paraDict):
        def singleFloatKey(f):
            return str(int(f * 100000000000000))
        intKey = "".join([str(i) for i in paraDict.get("I", [])])
        floKey = "".join([singleFloatKey(f) for f in paraDict.get("F", [])])
        return floKey + "_" + intKey


    def runJob(self, paramList:list[dict] | None=None) -> list:
        """submit parameters (if there is any) into backend and return results.

        Args:
            paramList (list, optional): element is dict ={'F':[],'I':[] } represents input args for circuit. Defaults to None.

        Returns:
            list: If paramList is None, return [result] (length of list is 1)
        """
        # ----- create isq source code
        self.make_isq_resource()
        if self.isInputParameter():
            if paramList is None:
                WarnStr = f"""This is a parameterized circuit, a submission must contains input parameters. Details see docs: \n\n {self.submit.__doc__}"""
                logging.error(WarnStr)
                raise CircuitError(WarnStr)
            else:
                """run job with parameters"""
                logging.debug(f"circuit: total num of jobs: {len(paramList)}")
                Return = []  # final return
                truelySubmit = []  # for those on caches, submit
                for i in range(len(paramList)):
                    para = paramList[i]
                    res = self._localstore.getdl( self._getParaKey(para) )
                    if res is None:
                        truelySubmit.append(para)
                        Return.append(len(truelySubmit) - 1)
                    else:
                        Return.append(res)
                logging.debug(f"[{len(truelySubmit)}] of them are not calculated")
                # ----- check renew resource
                # print(truelySubmit,6666)
                nF = len(paramList[0].get("F", []))
                nI = len(paramList[0].get("I", []))
                self._ir.precondition(nF=nF,nI=nI) 
                calcResults = self._backend.runJob_withParameters(paramList=truelySubmit)
                for i in range(len(Return)):
                    if type(Return[i]) is int:
                        Return[i] = calcResults[Return[i]]
                        self._localstore.setdl(key=self._getParaKey(paramList[i]), val=Return[i])
                return Return
        else:
            if paramList is not None:
                logging.warning(
                    "This circuit needs not input parameters, the external input parameters are ignored"
                )
            else:
                """run job without parameters"""
                # ----- check renew resource
                self._ir.precondition(nF=0,nI=0)
                result = self._backend.runJob_noParameter()
                return [result]
            
    def _lockMap(self,lockMap):
        # can contains a qMap. Can be used by deployer.
        # when this qMap is contained, following deployer when automatically load this qMap. lockMap is before qMap of deployer
        # self._islocked = False 
        # self._lockedMap = None
        self._islocked = True 
        self._lockedMap = list(lockMap)
        return self 
    
    def _hasLockedMap(self):
        return self._islocked
    
    def _getLockedMap(self):
        if not self._islocked:
            logging.warn("no locked map inside circuit. return None")
            return None
        else:
            return list(self._lockedMap)
        
    def _removeLockedMap(self):
        self._islocked = False

    def getqMap(self):
        # return circuit-qMap.
        return list(self.qMap)
    
    def getBackend(self):
        return self._backend
    

    def export_qiskit(self, F:list[float]|None=None,I:list[int]|None=None) -> QiskitCircuit:
        """export current gates (and measurement into qiskit circuit)

        Args:
            F (list[float] | None, optional): _description_. Defaults to None.
            I (list[int] | None, optional): _description_. Defaults to None.

        Returns:
            QiskitCircuit: _description_
        """     
        if QiskitCircuit is typing.Any:
            raise CircuitError("need install qiskit first")   
        if F is None:
            F = [] 
        if I is None:
            I = []     
        self.make_isq_resource()
        self._ir.precondition(nF=len(F),nI=len(I))   
        cirData = self._ir.dumpGates(F=F,I=I) 
        qMap = cirData['qMap']
        nq = cirData['n'] 
        nc = len(cirData['measurement'])
        circ=qiskit.QuantumCircuit(nq,nc)

        table_1g0p = {
            'H':'h',
            'X':'x',
            "Y":'y',
            "Z":'z',
            'S':'s',
            'T':'t',
            'SD':'sdg',
            'TD':'tdg',
        }
        table_1g1p = {
            'RZ':'rz',
            'RX':'rx',
            'RY':'ry',
        }
        table_2g0p = {
            'CX':'cx',
            'CY':'cy',
            'CZ':'cz',
            'CNOT':'cnot',
        }
        table_other = [
            'X2M','X2P','Y2M','Y2P'
        ]
        for gline in cirData['gates']:
            gName,iPara,fPara = gline 
            if gName in table_1g0p:
                getattr(circ,table_1g0p[gName])( qMap[iPara[0]] )
            elif gName in table_1g1p:
                getattr(circ,table_1g1p[gName])( fPara[0], qMap[iPara[0]] )
            elif gName in table_2g0p:
                getattr(circ,table_2g0p[gName])( qMap[iPara[0]], qMap[iPara[1]] )
            elif gName in table_other:
                if gName == 'X2M':
                    circ.rx(  -np.pi/2 , qMap[iPara[0]] )
                elif gName == 'X2P':
                    circ.rx(   np.pi/2 , qMap[iPara[0]] )
                elif gName == 'Y2M':
                    circ.ry(  -np.pi/2 , qMap[iPara[0]] )
                elif gName == 'Y2P':
                    circ.ry(   np.pi/2 , qMap[iPara[0]] )
            else:
                raise CircuitError(f"unkown gate = [{gName}]")
        circ.measure( [qMap[i] for i in cirData['measurement']] , range(nc) )
        return circ
        






    #---- some default gates ------
    def _LockedIndex(self,i):
        '''if there is a locked qMap, interal gate deployer must use it'''
        if self._hasLockedMap():
            return self._lockedMap[i] 
        else:
            return i 
        

    def H(self,i):
        self._defaultGate.H(self._LockedIndex(i))
        return self 
    
    def X(self,i):
        self._defaultGate.X(self._LockedIndex(i))
        return self 
    
    def Y(self,i):
        self._defaultGate.Y(self._LockedIndex(i)) 
        return self 

    def Z(self,i):
        self._defaultGate.Z(self._LockedIndex(i)) 
        return self 
    
    def S(self,i):
        self._defaultGate.S(self._LockedIndex(i)) 
        return self 
    
    def SD(self,i):
        self._defaultGate.SD(self._LockedIndex(i)) 
        return self 
    
    def T(self,i):
        self._defaultGate.T(self._LockedIndex(i))
        return self 

    def TD(self,i):
        self._defaultGate.TD(self._LockedIndex(i))
        return self 
    
    def Y2M(self,i):
        self._defaultGate.Y2M(self._LockedIndex(i))
        return self 
    
    def Y2P(self,i):
        self._defaultGate.Y2P(self._LockedIndex(i))
        return self 
    
    def X2M(self,i):
        self._defaultGate.X2M(self._LockedIndex(i))
        return self 
    
    def X2P(self,i):
        self._defaultGate.X2P(self._LockedIndex(i))
        return self 
    
    def Rx(self,i,theta):
        self._defaultGate.Rx(self._LockedIndex(i),theta)
    
    def Ry(self,i,theta):
        self._defaultGate.RY(self._LockedIndex(i),theta) 
        return self 
    
    def Rz(self,i,theta):
        self._defaultGate.RZ(self._LockedIndex(i),theta) 
        return self 
    
    def CNOT(self,i,j):
        self._defaultGate.CNOT(self._LockedIndex(i),self._LockedIndex(j)) 
        return self
    
    def CZ(self,i,j):
        self._defaultGate.CZ(self._LockedIndex(i),self._LockedIndex(j)) 
        return self
    
    def CX(self,i,j):
        return self.CNOT(i,j) 

