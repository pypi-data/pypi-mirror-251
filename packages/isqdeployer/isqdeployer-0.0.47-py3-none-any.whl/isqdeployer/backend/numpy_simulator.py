from __future__ import annotations

from isqtools.backend import NumpyBackend
from isqtools.circuits import IsqCircuit

from .abcBackend import Backend as BackendBaseClass

numpy_backend = NumpyBackend()


class Backend(BackendBaseClass):
    def __init__(self, *, shots: int | None = None, **kw) -> None:
        self.shots = shots
        BackendBaseClass.__init__(self, **kw)

    def get_QCIS(self, F=[], I=[], **kw):
        return self._getCircuit()._ir.getOutput_QCIS(F=F, I=I, **kw)

    def get_res(self, qcis: str) -> dict[str, float]:
        if self.shots is None:
            qc_isqtools = IsqCircuit(backend=numpy_backend, sample=False, qcis=qcis)
            res_list = qc_isqtools.measure()
        else:
            qc_isqtools = IsqCircuit(
                backend=numpy_backend,
                sample=True,
                shots=self.shots,
                qcis=qcis,
            )
            res_list = qc_isqtools.dict2array(
                qc_isqtools.sort_dict(qc_isqtools.measure())
            )
        return {
            bin(i)[2:].zfill(len(self.circuit.getMeasurementList())): prob
            for i, prob in enumerate(res_list)
            if prob > 1e-14
        }

    def runJob_noParameter(self) -> dict:
        qcisCode = self.get_QCIS()
        return self.get_res(qcis=qcisCode)

    def runJob_withParameters(self, paramList) -> list:
        if len(paramList) == 0:
            return []
        RETURN = []
        for para in paramList:
            qcisCode = self.get_QCIS(F=para.get("F", []), I=para.get("I", []))
            RETURN.append(self.get_res(qcis=qcisCode))
        return RETURN
