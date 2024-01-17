from __future__ import annotations

from abc import abstractmethod


class BackendError(Exception):
    """Backend error."""


class Backend:
    """Connect to backend, such as simulators and real devices.
    isq resource

    Returns:
        _type_: _description_

    """

    def __init__(self, **kw):
        self.isCreateIsQNeeded = None
        # flag to mark if recreate isq resource, children class may need this
        self.kw = kw

    def _setCircuit(self, circuit):
        self.circuit = circuit

    def _getCircuit(self):
        if hasattr(self, "circuit"):
            return self.circuit
        else:
            raise BackendError("backend has no attribute 'circuit' currently")

    def get_isqCache_pointer(self):
        return self.isqCache

    # -------------------------------------------------------------------------------

    @abstractmethod
    def runJob_noParameter(self) -> dict[str, float]:
        """run jon with parameters"""

    @abstractmethod
    def runJob_withParameters(self, paramList) -> list[dict[str, float]]:
        """run jon without parameters"""
