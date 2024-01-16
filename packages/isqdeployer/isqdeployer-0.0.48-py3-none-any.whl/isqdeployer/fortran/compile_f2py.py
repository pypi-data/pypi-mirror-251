#!/usr/bin/env python3

import os 
import sys 

PYTHON = sys.executable


cmd = f'{PYTHON} -m numpy.f2py -c circuit.sub.f90 -m fCircuit'

os.system(cmd)
