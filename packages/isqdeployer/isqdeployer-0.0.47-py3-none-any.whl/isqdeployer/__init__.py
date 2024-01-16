


import os,json  
# LIB_PATH = os.path.realpath(__file__)
LIB_PATH = os.path.dirname(__file__)
LIB_ENVIRON = {
    "LIB_PATH": LIB_PATH,
    "FORTRAN": os.path.join(LIB_PATH, "fortran"),
    "ISQ": os.path.join(LIB_PATH, "isQ"),
}
os.environ['LIB_ENVIRON'] = json.dumps(LIB_ENVIRON)


from .isQmaker import isQ_maker

# from .gateDeployer import *
from . import circuitDeployer


from .circuit import Circuit

from . import ansatz

from . import backend

from . import utils

# from .backend import *













