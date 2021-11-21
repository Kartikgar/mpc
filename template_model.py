# -*- coding: utf-8 -*-
"""
Created on Wed May 19 15:14:11 2021

@author: Kartik
"""

import numpy as np
import sys
from casadi import *
import do_mpc

def template_model():
    model_type = 'continuous'
    model = do_mpc.model.Model(model_type)
    m = 1 #mass of pendulum
    M = 5 #mass of cart
    L = 1
    g = 10
    pos = model.set_variable('_x', 'pos')
    theta = model.set_variable('_x', 'theta')
    dpos = model.set_variable('_x','dpos')
    dtheta = model.set_variable('_x','dtheta')
    u = model.set_variable('_u', 'force')
    
    #new algebraic states
    ddpos = model.set_variable('_z' , 'ddpos')
    ddtheta = model.set_variable('_z', 'ddtheta')
    
    model.set_rhs('pos', dpos)
    model.set_rhs('theta', dtheta)
    model.set_rhs('dpos', ddpos)
    model.set_rhs('dtheta', ddtheta)
    
    dynamic_eq = vertcat(
        #1
        ddpos*m*L**2*(M+m*(1-cos(theta)**2)) +
        (m**2*L**2*g*cos(theta)*sin(theta)-m*L**2*(m*L*dtheta**2*sin(theta)) - m*L**2*u),
        #2
        ddtheta*m*L**2*(M+m*(1-cos(theta)**2)) - 
        ((m+M)*m*g*L*sin(theta)- m*L*cos(theta)*(m*L*dtheta**2*sin(theta)) + m*L*cos(theta)*u)
        
        )
    model.set_alg('dynamic_system', dynamic_eq)
    
    #kinetic energy
    E_kin = dpos**2*(M+m)/2 + m*dpos*L*dtheta*cos(theta)/2 + (m*L**2*dtheta**2)/6 
    
    #potential energy
    E_pot = m*g*L*cos(theta)/2 
    model.set_expression('E_kin', E_kin)
    model.set_expression('E_pot', E_pot)
    model.setup()
    return model
    