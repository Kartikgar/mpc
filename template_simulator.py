# -*- coding: utf-8 -*-
"""
Created on Wed May 19 16:21:23 2021

@author: Kartik
"""

import numpy as np
import sys
from casadi import *
import do_mpc

def template_simulator(model):
    simulator= do_mpc.simulator.Simulator(model)
    params_simulator = {
    # Note: cvode doesn't support DAE systems.
    'integration_tool': 'idas',
    'abstol': 1e-10,
    'reltol': 1e-10,
    't_step': 0.04
}

    simulator.set_param(**params_simulator)
    simulator.setup()
    return simulator