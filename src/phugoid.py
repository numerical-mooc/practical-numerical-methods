# SPDX-License-Identifier: BSD-3-Clause

'''Previously introduced functions reused in the phugoid lessons.'''

import numpy as np


def rhs_full_phugoid(u, C_L, C_D, g, v_t):
    '''Return the derivatives for the nonlinear, damped phugoid model.

    Parameters
    ----------
    u : np.ndarray
        State vector [v, theta, x, y].
    C_L : float
        Lift coefficient.
    C_D : float
        Drag coefficient.
    g : float
        Gravitational acceleration.
    v_t : float
        Trim speed.

    Returns
    -------
    np.ndarray
        Derivative vector [dv/dt, dtheta/dt, dx/dt, dy/dt].
    '''
    v, theta, x, y = u
    return np.array([
        -g * np.sin(theta) - (C_D / C_L) * (g / v_t**2) * v**2,
        -(g / v) * np.cos(theta) + (g / v_t**2) * v,
        v * np.cos(theta),
        v * np.sin(theta),
    ])


def euler_step(u, f, dt, *args):
    '''Return the next state using one Forward Euler step.

    Parameters
    ----------
    u : np.ndarray
        State at the current time.
    f : callable
        Function that returns the state derivatives.
    dt : float
        Time-step size.
    *args
        Additional positional arguments passed to f.

    Returns
    -------
    np.ndarray
        State after one Forward Euler step.
    '''
    return u + dt * f(u, *args)


def discrete_l1_difference(
    q_coarse, q_fine, dt_coarse, dt_fine
):
    '''Return a discrete L1 difference on two nested time grids.'''
    refinement_ratio = int(round(dt_coarse / dt_fine))

    if not np.isclose(
        dt_coarse, refinement_ratio * dt_fine
    ):
        raise ValueError('Time-step sizes do not define nested grids.')

    q_fine_on_coarse_grid = q_fine[::refinement_ratio]

    if q_fine_on_coarse_grid.shape != q_coarse.shape:
        raise ValueError('Grid endpoints or sample counts do not align.')

    return dt_coarse * np.sum(
        np.abs(q_coarse - q_fine_on_coarse_grid)
    )
