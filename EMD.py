#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:45:11 2020
@author: veax-void
""" 

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def EMD(signal, max_imfs=3, min_std=0.3):
    '''
    Empirical Mode Decomposition
    max_imfs - number of Intrinsic mode functions (IMF)
    min_std - std of final function. Stoping condition
    '''

    c = signal
    IMFs = []

    for n in range(max_imfs):
        h = c
        std = 1
        while std > min_std:
            maxenv, minenv = max_min_env(h)
            # If can't find min/max points, exit
            if (type(maxenv) == int or type(minenv) == int):
                break

            # Mean of max and min enveloppes
            meanenv = (maxenv + minenv) / 2

            # Copy of the previous value of h before modifying it
            prev_h = h.copy()

            h = h - meanenv

            # Calculate standard deviation
            eps = 0.0000001 # to avoid zero values
            std = sum(((prev_h - h)**2) / (prev_h**2 + eps))

        IMFs += [h]

        c = c - h

    return IMFs


def max_min_env(signal):
    d = np.diff(signal)
    N = len(signal)
    t = np.arange(0,N)

    maxmin = []

    # Find local max/min points
    for i in range(N-2):
        if d[i] == 0:
            if np.sign(d[i-1]) != np.sign(d[i+1]):
                maxmin += [i]

        elif np.sign(d[i]) != np.sign(d[i+1]):
            maxmin += [i+1]

    if len(maxmin) <= 2:
        return -1, -1

    # Divide maxmin into maxes and mins
    if maxmin[0] > maxmin[1]:
        maxes = maxmin[0::2]
        mins = maxmin[1::2]
    else:
        maxes = maxmin[1::2]
        mins = maxmin[0::2]

    # Fix endpoints
    maxes.insert(0,0)
    maxes.append(N-1)
    mins.insert(0,0)
    mins.append(N-1)

    # Spline interpolate for max and min envelopes, form imf
    maxenv_cs = CubicSpline(maxes, signal[maxes])
    minenv_cs = CubicSpline(mins, signal[mins])

    maxenv = maxenv_cs(t)
    minenv = minenv_cs(t)

    return maxenv, minenv


def plot_imfs(imfs):
    fig, ax = plt.subplots(len(imfs), 1)
    for i in range(len(imfs)):
        ax[i].plot(imfs[i])
    fig.tight_layout()
