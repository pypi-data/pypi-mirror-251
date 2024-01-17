from __future__ import annotations

import multiprocessing

import numpy as np

from .abcBackend import Backend as BackendBaseClass
from .abcBackend import BackendError


class InteractiveBackendError(BackendError):
    """Interactive backend error"""


def _nCoreFunc(args):
    self = args[0]
    para = args[1]
    return self.claculateCircuit(F=para.get("F", []), I=para.get("I", []))


class InteractiveBackend(BackendBaseClass):
    """
    Simulator backend

    Args:
        circuit (Circuit): _description_
        workDir (str, None): _description_. Defaults to None.
        nCore (int,1): for parallel calculation.

    """

    def __init__(self, nCore: int = 1, **kw):
        self.nCore = nCore
        BackendBaseClass.__init__(self, **kw)

    def runJob_noParameter(self) -> dict:
        return self.claculateCircuit(F=[], I=[])

    def runJob_withParameters(self, paramList) -> list:
        if len(paramList) == 0:
            return []
        nCore = self.nCore
        if nCore > 1:
            with multiprocessing.Pool(nCore) as p:
                res = p.map(_nCoreFunc, [[self, para] for para in paramList])
                return res
        else:
            RETURN = []
            for para in paramList:
                RETURN.append(
                    self.claculateCircuit(F=para.get("F", []), I=para.get("I", []))
                )
            return RETURN

    def claculateCircuit(self, F, I):
        def getbitFiled(n, L):
            result = np.binary_repr(n, L)
            r = [int(digit) for digit in result]
            r.reverse()
            return r

        dumpInfo = self._getCircuit()._ir.dumpGates(F=F, I=I)
        nq = dumpInfo["n"]
        measureList = dumpInfo["measurement"]
        gates = dumpInfo["gates"]
        qMap = dumpInfo["qMap"]
        self.initCalc(nq=nq, qMap=qMap)
        for gate in gates:
            gateName, iParams, fParams = gate
            if gateName in (
                "H",
                "X",
                "Y",
                "Z",
                "S",
                "T",
                "SD",
                "TD",
                "X2M",
                "X2P",
                "Y2M",
                "Y2P",
            ):
                getattr(self, gateName)(iParams[0])
            elif gateName in ("RZ", "RX", "RY"):
                getattr(self, gateName)(iParams[0], fParams[0])
            elif gateName in ("CZ", "CX", "CY"):
                getattr(self, gateName)(iParams[0], iParams[1])
            else:
                raise InteractiveBackendError(f"Undefined gatenName = {gateName}")
        self.finalCalc()
        # ------------------
        # if getFinalState is defined, it can be called here
        res = self.getFullProb()
        # measureList
        R = {}
        zero = 1e-14
        for i in res:
            bitField = getbitFiled(n=int(i), L=nq)
            R_key = "".join([str(bitField[q]) for q in measureList])
            if res[i] > zero:
                if R_key not in R:
                    R[R_key] = 0
                R[R_key] += res[i]
        return R

    # ---------------------------------------------
    def initCalc(self, nq, qMap):
        """nq is total number of qubit"""

    def finalCalc(self):
        """"""

    def getFinalState(self) -> list[complex]:
        """
        return complex [0:2**n-1]
        """
        raise InteractiveBackendError("Not implemented")

    def getFullProb(self) -> dict:
        """
        if getFinalState can be implemented, no need to redefine getFullProb
        """
        vec = self.getFinalState()
        res = {}
        for i in range(len(vec)):
            res[i] = (vec[i] * vec[i].conjugate()).real
        return res

    def X(self, i):
        raise InteractiveBackendError("Not implemented")

    def H(self, i):
        raise InteractiveBackendError("Not implemented")

    def Y(self, i):
        raise InteractiveBackendError("Not implemented")

    def Z(self, i):
        raise InteractiveBackendError("Not implemented")

    def S(self, i):
        raise InteractiveBackendError("Not implemented")

    def T(self, i):
        raise InteractiveBackendError("Not implemented")

    def SD(self, i):
        raise InteractiveBackendError("Not implemented")

    def TD(self, i):
        raise InteractiveBackendError("Not implemented")

    def X2M(self, i):
        raise InteractiveBackendError("Not implemented")

    def X2P(self, i):
        raise InteractiveBackendError("Not implemented")

    def Y2M(self, i):
        raise InteractiveBackendError("Not implemented")

    def Y2P(self, i):
        raise InteractiveBackendError("Not implemented")

    def RX(self, i, phi):
        raise InteractiveBackendError("Not implemented")

    def RY(self, i, phi):
        raise InteractiveBackendError("Not implemented")

    def RZ(self, i, phi):
        raise InteractiveBackendError("Not implemented")

    def CX(self, i, j):
        raise InteractiveBackendError("Not implemented")

    def CY(self, i, j):
        raise InteractiveBackendError("Not implemented")

    def CZ(self, i, j):
        raise InteractiveBackendError("Not implemented")
