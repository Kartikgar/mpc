# -*- coding: utf-8 -*-
"""
Created on Wed May 19 16:33:01 2021

@author: Kartik
"""

from template_model import template_model
from template_mpc import template_mpc
from template_simulator import template_simulator
import numpy as np
import sys
from casadi import *
import do_mpc

model = template_model()
mpc = template_mpc(model)
simulator = template_simulator(model)
estimator = do_mpc.estimator.StateFeedback(model)

simulator.x0['theta'] = 0.19*np.pi

x0 = simulator.x0.cat.full()

mpc.x0 = x0
estimator.x0 = x0

mpc.set_initial_guess()
import matplotlib.pyplot as plt
plt.ion()
from matplotlib import rcParams
rcParams['text.usetex'] = False
rcParams['axes.grid'] = True
rcParams['lines.linewidth'] = 2.0
rcParams['axes.labelsize'] = 'xx-large'
rcParams['xtick.labelsize'] = 'xx-large'
rcParams['ytick.labelsize'] = 'xx-large'
mpc_graphics = do_mpc.graphics.Graphics(mpc.data)


def pendulum_bars(x):
    x = x.flatten()
    L=1
    # Get the x,y coordinates of the two bars for the given state x.
    line_1_x = np.array([
        x[0],
        x[0]+L*np.sin(x[1])
    ])

    line_1_y = np.array([
        0,
        L*np.cos(x[1])
    ])

    #line_2_x = np.array([
        #line_1_x[1],
        #line_1_x[1] + L2*np.sin(x[2])
    #])

    #ine_2_y = np.array([
        #line_1_y[1],
        #line_1_y[1] + L2*np.cos(x[2])
    #])

    line_1 = np.stack((line_1_x, line_1_y))
    #line_2 = np.stack((line_2_x, line_2_y))

    return line_1


fig = plt.figure(figsize=(16,9))

ax1 = plt.subplot2grid((4, 2), (0, 0), rowspan=4)
ax2 = plt.subplot2grid((4, 2), (0, 1))
ax3 = plt.subplot2grid((4, 2), (1, 1))
ax4 = plt.subplot2grid((4, 2), (2, 1))
ax5 = plt.subplot2grid((4, 2), (3, 1))

ax2.set_ylabel('$E_{kin}$ [J]')
ax3.set_ylabel('$E_{pot}$ [J]')
ax4.set_ylabel('Angle  [rad]')
ax5.set_ylabel('Input force [N]')

# Axis on the right.
for ax in [ax2, ax3, ax4, ax5]:
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    if ax != ax5:
        ax.xaxis.set_ticklabels([])

ax5.set_xlabel('time [s]')

mpc_graphics.add_line(var_type='_aux', var_name='E_kin', axis=ax2)
mpc_graphics.add_line(var_type='_aux', var_name='E_pot', axis=ax3)
mpc_graphics.add_line(var_type='_x', var_name='theta', axis=ax4)
mpc_graphics.add_line(var_type='_u', var_name='force', axis=ax5)

ax1.axhline(0,color='black')

bar1 = ax1.plot([],[], '-o', linewidth=5, markersize=10)
bar2 = ax1.plot([],[], '-o', linewidth=5, markersize=10)

ax1.set_xlim(-1.8,1.8)
ax1.set_ylim(-1.2,1.2)
ax1.set_axis_off()
#u0 = mpc.make_step(x0)

#fig.align_ylabels()
#line1 = pendulum_bars(x0)
#bar1[0].set_data(line1[0],line1[1])
#bar2[0].set_data(line2[0],line2[1])
#mpc_graphics.plot_predictions()
#mpc_graphics.reset_axes()

#fig
mpc.reset_history()

n_steps = 100
for k in range(n_steps):
    u0 = mpc.make_step(x0)
    y_next = simulator.make_step(u0)
    x0 = estimator.make_step(y_next)
    
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

# The function describing the gif:
x_arr = mpc.data['_x']
def update(t_ind):
    line1 = pendulum_bars(x_arr[t_ind])
    bar1[0].set_data(line1[0],line1[1])
    #bar2[0].set_data(line2[0],line2[1])
    mpc_graphics.plot_results(t_ind)
    mpc_graphics.plot_predictions(t_ind)
    mpc_graphics.reset_axes()
    


anim = FuncAnimation(fig, update, frames=n_steps, repeat=False)
gif_writer = PillowWriter(fps=20)
anim.save('anim_cartpole2.gif', writer=gif_writer)