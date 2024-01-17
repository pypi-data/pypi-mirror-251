from .circuit import Circuit
from .intermediateRepresentation import QcisParser


class Importer():


    def qcis2circuit(qcisStr:str,circuitConfig:dict={}):
        """_summary_

        Args:
            qcisStr (str): qcis string
            circuit (Circuit): circuit object

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """        
        parser = QcisParser(qcisStr) 
        nq = parser.getNq()
        qMap = parser.getMap()
        glines = parser.exportGates()
        table_1g0p = {
            'H':'H',
            'X':'X',
            "Y":'Y',
            "Z":'Z',
            'S':'S',
            'T':'T',
            'SD':'SD',
            'TD':'TD',
            'X2M':'X2M',
            'X2P':'X2P',
            'Y2M':'Y2M',
            'Y2P':'Y2P',
        }
        table_1g1p = {
            'RZ':'Rz',
            'RX':'Rx',
            'RY':'Ry',
        }
        table_2g0p = {
            'CX':'CNOT',
            'CY':'CY',
            'CZ':'CZ',
            'CNOT':'CNOT',
        }
        table_other = [
            
        ]

        circuit = Circuit(nq=nq,**circuitConfig)
        for gline in glines:
            gName,iPara,fPara = gline 
            if gName in table_1g0p:
                getattr(circuit,table_1g0p[gName])( qMap[iPara[0]] )
            elif gName in table_1g1p:
                getattr(circuit,table_1g1p[gName])( qMap[iPara[0]], fPara[0] )
            elif gName in table_2g0p:
                getattr(circuit,table_2g0p[gName])( qMap[iPara[0]], qMap[iPara[1]] )
            elif gName in table_other:
                pass 
            else:
                raise Exception(f"unkown gate = [{gName}]")
        circuit.setMeasurement( [ qMap[i] for i in parser.getMeasurements() ] )
        return circuit
