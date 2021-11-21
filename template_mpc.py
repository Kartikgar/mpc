# -*- coding: utf-8 -*-
"""
Created on Wed May 19 16:09:40 2021

@author: Kartik
"""

import numpy as np
import sys
from casadi import *
import do_mpc

def template_mpc(model):
    mpc = do_mpc.controller.MPC(model)
    setup_mpc = {
    'n_horizon': 100,
    'n_robust': 0,
    'open_loop': 0,
    't_step': 0.04,
    'state_discretization': 'collocation',
    'collocation_type': 'radau',
    'collocation_deg': 3,
    'collocation_ni': 1,
    'store_full_solution': True,
    # Use MA27 linear solver in ipopt for faster calculations:
    'nlpsol_opts': {'ipopt.linear_solver': 'mumps'}
}
    mpc.set_param(**setup_mpc)
    mterm=model.aux['E_kin'] - model.aux['E_pot'] #terminal cost
    lterm = model.aux['E_kin'] - model.aux['E_pot']
    mpc.set_objective(mterm=mterm, lterm=lterm)
    mpc.set_rterm(force=0.1)
    mpc.bounds['lower','_u','force'] = -4
    mpc.bounds['upper','_u','force'] = 4
    mpc.setup()
    return mpc