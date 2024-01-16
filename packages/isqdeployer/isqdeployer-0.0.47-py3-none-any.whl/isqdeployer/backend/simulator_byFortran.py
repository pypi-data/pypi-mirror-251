from __future__ import annotations

import json
import os
import shutil
import sys

import numpy as np

from .abcInteractiveBackend import InteractiveBackend

fortranDir = json.loads(os.environ["LIB_ENVIRON"])["FORTRAN"]
sys.path.append(fortranDir)


class NoneFortranCompilerError(Exception):
    """No Fortran compiler."""


def isGfortranInstalled():
    return shutil.which("gfortran") is not None


try:
    import fCircuit
except:
    if isGfortranInstalled():
        PYTHON = sys.executable
        cwd = os.getcwd()
        os.chdir(fortranDir)
        os.system(f"{PYTHON} compile_f2py.py")
        os.chdir(cwd)
        import fCircuit
    else:
        raise NoneFortranCompilerError("gfortran is required")


class Backend(InteractiveBackend):
    def append(self, iPara=[], fPara=[]):
        IP = iPara + [0] * (self.iParaLen - len(iPara))
        FP = fPara + [0.0] * (self.fParaLen - len(fPara))
        self.iParaList.append(IP)
        self.fParaList.append(FP)
        return self

    # ---------------------------------------------
    def initCalc(self, nq, qMap):
        self.nq = nq
        self.iParaList = []
        self.fParaList = []
        self.iParaLen = 4
        self.fParaLen = 1

    def getFinalState(self) -> list[complex]:
        """
        return complex [0:2**n-1]
        """
        IP = np.array(self.iParaList).reshape(-1)
        FP = np.array(self.fParaList).reshape(-1)
        d = 2**self.nq
        nGates = len(self.iParaList)
        vec = fCircuit.simulatecircuit(d, nGates, IP, FP)
        return vec

    def X(self, i):
        return self.append(iPara=[0, i])

    def Y(self, i):
        return self.append(iPara=[1, i])

    def Z(self, i):
        return self.append(iPara=[2, i])

    def H(self, i):
        return self.append(iPara=[3, i])

    def S(self, i):
        return self.append(iPara=[4, i])

    def T(self, i):
        return self.append(iPara=[5, i])

    def Rx(self, i, phi):
        return self.append(iPara=[6, i], fPara=[phi])

    def Ry(self, i, phi):
        return self.append(iPara=[7, i], fPara=[phi])

    def Rz(self, i, phi):
        return self.append(iPara=[8, i], fPara=[phi])

    def RX(self, i, phi):
        return self.Rx(i, phi)

    def RY(self, i, phi):
        return self.Ry(i, phi)

    def RZ(self, i, phi):
        return self.Rz(i, phi)

    def X2P(self, i):
        return self.Rx(i, np.pi / 2)

    def X2M(self, i):
        return self.Rx(i, -np.pi / 2)

    def Y2P(self, i):
        return self.Ry(i, np.pi / 2)

    def Y2M(self, i):
        return self.Ry(i, -np.pi / 2)

    def SD(self, i):
        return self.append(iPara=[9, i])

    def TD(self, i):
        return self.append(iPara=[10, i])

    def CX(self, i, j):
        return self.append(iPara=[100, i, j])

    def CZ(self, i, j):
        return self.append(iPara=[101, i, j])
