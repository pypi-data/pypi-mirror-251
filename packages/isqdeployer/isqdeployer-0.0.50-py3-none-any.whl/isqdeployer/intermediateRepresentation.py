from __future__ import annotations
import os 
# from .backend.abcBackend import LimitedSizeDict
from .utils.cacheStore import CacheStore
from .utils.fasthash import fasthash
import pyisqc
from pyisqc.utils import FindSimulator



class IRERROR(Exception):pass 

# from collections import OrderedDict


# class LimitedSizeDict(OrderedDict):
#     """Store cache of simulation."""

#     default_len = 100

#     def __init__(self, *args, **kw):
#         self.size_limit = kw.pop("maxlen", self.default_len)
#         OrderedDict.__init__(self, *args, **kw)
#         self._check_size_limit()

#     def __setitem__(self, key, value):
#         OrderedDict.__setitem__(self, key, value)
#         self._check_size_limit()

#     def _check_size_limit(self):
#         if self.size_limit is not None:
#             while len(self) > self.size_limit:
#                 self.popitem(last=False)





class abcIntermediateRepresentation():
    '''
    input:isq, output: other representations
    '''

    def __init__(self,isqPath:str,cacheStore:CacheStore,workDir:str|None=None):
        self._isqPath = isqPath 
        self.cacheStore = cacheStore
        self._SimulatorBIN = FindSimulator().get_simulatorBIN_path()
        if workDir is None:
            self._workDir = self._get_isq_dir() 
        else:
            self._workDir = workDir

    def _get_isq_dir(self):
        return os.path.dirname(os.path.abspath(self._isqPath))
    
    def _get_isq_hash(self):
        with open(self._isqPath, "r") as f:
            return fasthash(f.read())

    def precondition(self,nF,nI):
        '''
        - This method will check if isq program is updated. If so, call renew_IR_resource
        - Before method <getOutput_***> is called, this function must be called once and (only once!), args F and I must also match <getOutput_***>
        '''
        needUpdate = self.cacheStore.get('IR_needupdate')
        if needUpdate:
            self.renew_IR_resource(nF,nI)
            self.cacheStore.set('IR_needupdate',False)
    #--------------------------------------------------------

    def renew_IR_resource(self,nF,nI):
        '''
        this method is called by precondition. 
        WARNING: Parallel calculation can only call this once.
        '''
        raise Exception("not implemented") 

    def dumpGates(self,F,I)->dict:
        '''
        {
            'n':nq,
            'gates': [ <gateName>, [intParams], [floatParams] ],
            'measurement':[],
            'qMap':[],
        }
        used for interactive backend
        '''
        raise Exception("not implemented") 

    def getOutput_QCIS(self, F=[], I=[], **kw)->str:
        raise Exception("not implemented") 
    
    def getOutput_QASM2(self, F=[], I=[], **kw)->str:
        raise Exception("not implemented") 
    

class QcisParserError(Exception):
    """Uni parser error."""

class QcisParser:
    """Qcis parser: isqc compile xxx.isq --target qcis """
    _pre_defined_gates = [
        "X",
        "Y",
        "Z",
        "H",
        "S",
        "T",
        "SD",
        "TD",
        "CZ",
        "X2M",
        "X2P",
        "Y2M",
        "Y2P",
        "RX",
        "RY",
        "RZ",
        "RXY",
        "M",
    ]

    def __init__(self, qcis_str: str) -> None:
        # print(qcis_str)
        self._qdic = {}
        self._qnum = 0
        self._mq = []
        self._gates = []
        self._get_gates(qcis_str)

    def _get_gates(self, qcis_str: str) -> None:
        for line in qcis_str.split("\n"):
            line = line.strip()
            if not line:
                continue
            data_per_line = line.split(" ")
            if data_per_line[0] not in self._pre_defined_gates:
                raise QcisParserError(
                    f"{data_per_line[0]} gate is not supported."
                )
                # only check gate name!
            if data_per_line[1] not in self._qdic:
                self._qdic[data_per_line[1]] = self._qnum
                self._qnum += 1
            if data_per_line[0] in ["CZ"]:
                if data_per_line[2] not in self._qdic:
                    self._qdic[data_per_line[2]] = self._qnum
                    self._qnum += 1

            qid1 = self._qdic[data_per_line[1]]
            if data_per_line[0] == "M":
                self._mq.append(qid1)
            else:
                if data_per_line[0] in ["CZ"]:
                    qid2 = self._qdic[data_per_line[2]]
                    self._gates.append((data_per_line[0], (qid1, qid2), None))
                elif data_per_line[0] in ["RX", "RY", "RZ", "RXY"]:
                    self._gates.append(
                        (
                            data_per_line[0],
                            (qid1,),
                            tuple(float(v) for v in data_per_line[2:]),
                        )
                    )
                else:
                    self._gates.append((data_per_line[0], (qid1,), None))

    def getNq(self) -> int:
        """return number of effective qubits"""
        return self._qnum

    def exportGates(self) -> list[tuple[str, tuple[int], tuple[float] | None]]:
        """return [ <gateName>, [intParams], [floatParams] ]"""
        return self._gates

    def getMeasurements(self) -> list[int]:
        """return list of index of qubit for final measurement"""
        return self._mq

    def getMap(self) -> list[int]:
        return [int(i[1:]) for i in self._qdic]


class UniParserError(Exception):
    """Uni parser error."""

class UniParser:
    """Uni parser
    right now support X, Y, Z, H, S, T, U3, CZ, CNOT, X2P, Y2P, X2M, Y2M, RX,
    RY, RZ, M...
    isqc compile xxx.isq --target uni
    """
    _pre_defined_gates = [
        "X",
        "Y",
        "Z",
        "H",
        "S",
        "T",
        "U3",
        "CZ",
        "CNOT",
        "X2M",
        "X2P",
        "Y2M",
        "Y2P",
        "RX",
        "RY",
        "RZ",
        "M",
    ]

    def __init__(self, uni_str: str) -> None:
        self._qdic = {}
        self._qnum = 0
        self._mq = []
        self._gates = []
        self._get_gates(uni_str)

    def _get_gates(self, uni_str: str) -> None:
        for line in uni_str.split("\n"):
            line = line.strip()
            if not line:
                continue
            data_per_line = line.split(" ")
            if data_per_line[0] not in self._pre_defined_gates:
                raise UniParserError(
                    f"{data_per_line[0]} gate is not supported."
                )
                # only check gate name!
            if data_per_line[1] not in self._qdic:
                self._qdic[data_per_line[1]] = self._qnum
                self._qnum += 1
            if data_per_line[0] in ["CZ", "CNOT"]:
                if data_per_line[2] not in self._qdic:
                    self._qdic[data_per_line[2]] = self._qnum
                    self._qnum += 1

            qid1 = self._qdic[data_per_line[1]]
            if data_per_line[0] == "M":
                self._mq.append(qid1)
            else:
                if data_per_line[0] in ["CZ", "CNOT"]:
                    qid2 = self._qdic[data_per_line[2]]
                    self._gates.append((data_per_line[0], (qid1, qid2), None))
                elif data_per_line[0] in ["RX", "RY", "RZ", "U3"]:
                    self._gates.append(
                        (
                            data_per_line[0],
                            (qid1,),
                            tuple(float(v) for v in data_per_line[2:]),
                        )
                    )
                else:
                    self._gates.append((data_per_line[0], (qid1,), None))

    def getNq(self) -> int:
        """return number of effective qubits"""
        return self._qnum

    def exportGates(self) -> list[tuple[str, tuple[int], tuple[float] | None]]:
        """return [ <gateName>, [intParams], [floatParams] ]"""
        return self._gates

    def getMeasurements(self) -> list[int]:
        """return list of index of qubit for final measurement"""
        return self._mq

    def getMap(self) -> list[int]:
        return [int(i[1:]) for i in self._qdic]


class IR_based_on_QCIS(abcIntermediateRepresentation):

    def getOutput_QCIS(self, F=[], I=[], **kw):
        self.FAKE_SO = self._get_qcis_SO_filePath()
        cwd = os.getcwd()
        os.chdir(self._workDir)
        QCIS = pyisqc._gen_qcis_from_so(
            file=self.FAKE_SO,
            int_param=I,
            double_param=F,
        )
        os.chdir(cwd)
        return QCIS
    
    def _get_qcis_SO_filePath(self):
        isqPath = self._isqPath
        return isqPath.replace(".isq", "_QCIS_TMP_.so")

    def renew_IR_resource(self, nF,nI) -> str:
        """create files without checking exist"""
        # fakeSO = os.path.join(self.getsoDir(), self.get_qcis_SO_fileName())
        fakeSO = self._get_qcis_SO_filePath() 

        passF = [1.0] * nF
        passI = [1] * nI # may be conflict
        cwd = os.getcwd()
        os.chdir(self._workDir)
        code, stdout, stderr = pyisqc.compile(
            file=self._isqPath,
            target="qcis",
            int_param=passI,
            double_param=passF,
            output=fakeSO,
        )
        #TODO: Error code need more info
        if code != 0:
            raise RuntimeError("Compile failed.")
        os.chdir(cwd)

    def dumpGates(self,F,I)->list:
        qcisStr = self.getOutput_QCIS(F=F,I=I) 
        paser = QcisParser(qcisStr) 
        nq = paser.getNq()
        gates = paser.exportGates() 
        measurement = paser.getMeasurements() 
        qMap = paser.getMap()
        return {
            'n':nq,
            'gates':gates,
            'measurement':measurement,
            'qMap':qMap,
        }
    




