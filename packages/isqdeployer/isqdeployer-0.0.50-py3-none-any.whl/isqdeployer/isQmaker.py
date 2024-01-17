import numpy as np
import logging


class isQ_maker:
    @staticmethod
    def define1DArray(type, varName, List):
        vStr = ",".join([str(i) for i in List])
        R = f"{type} {varName} [] = "
        R += "[" + vStr + "];"
        return R

    @classmethod
    def autoSetArray(cls, varName, data):
        # set array in any shape into 1D array automatically.
        d = np.array(data)
        npType = str(d.dtype)
        if "int" in npType:
            Type = "int"
        elif "float" in npType:
            Type = "double"
        else:
            logging.error(f"Unsupported type = {npType}")
        return cls.define1DArray(type=Type, varName=varName, List=d.reshape(-1))
