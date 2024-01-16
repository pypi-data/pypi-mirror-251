from __future__ import annotations

from .abcInteractiveBackend import InteractiveBackend


import numpy as np 

from qiskit import QuantumCircuit,transpile
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
from qiskit_aer import AerSimulator

class Backend(InteractiveBackend):
    '''https://qiskit.org/ecosystem/aer/tutorials/3_building_noise_models.html'''

    def __init__(self,shots=2000,fidelity_1q:float=1.0,fidelity_2q=1.0,fidelity_measure=1.0,**kw):

        noise_model = NoiseModel()
        error_1q = depolarizing_error(1-fidelity_1q, num_qubits=1)
        error_2q = depolarizing_error(1-fidelity_2q, num_qubits=2)
        error_me = pauli_error([('X',1-fidelity_measure), ('I', fidelity_measure )])

        noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3',])
        noise_model.add_all_qubit_quantum_error(error_2q, [ 'cz'])
        noise_model.add_all_qubit_quantum_error(error_me, "measure")
        # Create noisy simulator backend
        self._INTERNAL_sim_noise = AerSimulator(noise_model=noise_model)
        self._INTERNAL_shots = shots

        super().__init__(**kw)

    #---------------------------------------------
    def initCalc(self,nq,qMap):
        self._INTERNAL_circuit = QuantumCircuit(nq)



    def finalCalc(self):
        self._INTERNAL_circuit.measure_all()
        circ_tnoise = transpile(self._INTERNAL_circuit, self._INTERNAL_sim_noise)
        result_noise = self._INTERNAL_sim_noise.run(circ_tnoise,shots=self._INTERNAL_shots).result()
        # print(result_noise,666)
        # print(result_noise.result,666)
        self._INTERNAL_resCount = result_noise.get_counts(0)



    
    # def getFinalState(self) ->list[complex]:
    #     '''
    #     return complex [0:2**n-1]
    #     '''
    #     raise SimulatorError("Not implemented")
    
    def getFullProb(self)->dict:
        '''
        if getFinalState can be implemented, no need to redefine getFullProb
        '''
        count = self._INTERNAL_resCount
        Ntot = 0 
        for k in count:
            Ntot += count[k] 
        res = {} 
        for k in count:
            res[int(k,2)] = count[k]*1.0 / Ntot
        return res
            
    def X(self,i):
        self._INTERNAL_circuit.x(i)
    
    def H(self,i):
        self._INTERNAL_circuit.h(i)
    
    def Y(self,i):
        self._INTERNAL_circuit.y(i)
    
    def Z(self,i):
        self._INTERNAL_circuit.z(i)
    
    def S(self,i):
        self._INTERNAL_circuit.s(i)
    
    def T(self,i):
        self._INTERNAL_circuit.t(i)
    
    def SD(self,i):
        self._INTERNAL_circuit.sdg(i)
    
    def TD(self,i):
        self._INTERNAL_circuit.tdg(i)

    def X2M(self,i):
        self._INTERNAL_circuit.rx(-np.pi/2,i)     

    def X2P(self,i):
        self._INTERNAL_circuit.rx(np.pi/2,i)
    
    def Y2M(self,i):
        self._INTERNAL_circuit.ry(-np.pi/2,i)

    def Y2P(self,i):
        self._INTERNAL_circuit.ry(np.pi/2,i)
    
    def RX(self,i,phi):
        self._INTERNAL_circuit.rx(phi,i)
    
    def RY(self,i,phi):
        self._INTERNAL_circuit.ry(phi,i)
    
    def RZ(self,i,phi):
        self._INTERNAL_circuit.rz(phi,i)
    
    def CX(self,i,j):
        self._INTERNAL_circuit.cx(i,j)
    
    def CY(self,i,j):
        self._INTERNAL_circuit.cy(i,j)
    
    def CZ(self,i,j):
        self._INTERNAL_circuit.cz(i,j)
    


