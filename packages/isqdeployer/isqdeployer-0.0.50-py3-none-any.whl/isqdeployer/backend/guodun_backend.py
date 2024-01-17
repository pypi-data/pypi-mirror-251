from __future__ import annotations

from collections.abc import Iterable

from isqtools.backend import QcisBackend
from isqtools.circuits import IsqCircuit

from .abcBackend import Backend as BackendBaseClass
from .abcBackend import BackendError


class Backend(BackendBaseClass):
    def __init__(
        self,
        login_key: str,
        machine_name: str = "gd_qc1",
        lab_id: int | None = None,
        exp_name: str | None = None,
        remark: str = "arclight",
        max_wait_time: int = 60,
        sleep_time: int = 3,
        run_time: int | None = None,
        mapping: bool = False,
        shots: int | None = None,
        is_prob: bool = False,
        logger=None,
        **kw,
    ) -> None:
        self.shots = shots
        self.login_key = login_key
        self.machine_name = machine_name
        self.lab_id = lab_id
        self.exp_name = exp_name
        self.remark = remark
        self.max_wait_time = max_wait_time
        self.sleep_time = sleep_time
        self.run_time = run_time
        self.mapping = mapping
        self.is_prob = is_prob
        self.logger = logger
        BackendBaseClass.__init__(self, **kw)
        self.is_login: bool = False

    def _check_login(self) -> None:
        if not self.is_login:
            self.guodun_backend = QcisBackend(
                login_key=self.login_key,
                machine_name=self.machine_name,
                lab_id=self.lab_id,
                exp_name=self.exp_name,
                remark=self.remark,
                max_wait_time=self.max_wait_time,
                sleep_time=self.sleep_time,
                run_time=self.run_time,
                mapping=self.mapping,
                is_prob=self.is_prob,
                logger=self.logger,
            )
            self.is_login = True

    def get_QCIS(self, F=[], I=[], **kw) -> str:
        return self._getCircuit()._ir.getOutput_QCIS(F=F, I=I, **kw)

    def get_res(self, qcis: str) -> dict[str, float]:
        if self.shots is None:
            raise BackendError("Shot number is required.")
        else:
            qc_isqtools = IsqCircuit(
                backend=self.guodun_backend,
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

    def runJob_noParameter(self) -> dict[str, int]:
        self._check_login()
        qcisCode = self.get_QCIS()
        return self.get_res(qcis=qcisCode)

    def runJob_withParameters(self, paramList: Iterable) -> list[dict[str, int]]:
        self._check_login()
        if len(paramList) == 0:
            return []
        RETURN = []
        for para in paramList:
            qcisCode = self.get_QCIS(F=para.get("F", []), I=para.get("I", []))
            RETURN.append(self.get_res(qcis=qcisCode))
        return RETURN
