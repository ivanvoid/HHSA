#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:15:55 2020

@author: veax-void

https://pyhht.readthedocs.io/en/latest/tutorials/hilbert_view_nonlinearity.html


!!! Under construction !!!


"""
# In[Init signals]
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
np.random.seed(1615552020)

from EMD import EMD, plot_imfs, max_min_env

N = 700

t = np.arange(0,N)
signal1 = np.sin(t * 0.1)
signal2 = np.sin(t * 0.2)
noise = np.random.uniform(-1,1,N)

# plt.plot(t, noise)
# plt.plot(t, signal)

spn = signal1+noise
smn = signal1*noise

sps = signal1 * signal2

signal = sps


plt.plot(t, signal, 'k-', label='data')

imfs = EMD(signal, 5)
plot_imfs(imfs)

# max_envs = []
# for imf in imfs:
#     max_env, _ = max_min_env(imf)
#     max_envs += [max_env]

# new_imfs = []
# for env in max_envs:
#     new_imfs += EMD(env,5)

# plot_imfs(new_imfs)

# In[]
inst_freq = []
for imf in imfs:
    h = hilbert(imf)
    omega = np.unwrap(np.angle(h))
    inst_freq += [np.diff(omega)]


imfs = new_imfs
# I need 2d array
z = []
for i in t:
    z.append([])
    for j in range(200):
        z[-1].append(0)

for n in range(3):
    for i in t:
        a = int(round(imfs[n][i] * 100))
        if a > 0 and a < 100:
            z[i][a+100] = inst_freq[n][i]
        elif a < 0 and a > -100:
            z[i][100 + a] = inst_freq[n][i]


z = np.array(z).T
im = plt.contourf(z)

# In[]
h = hilbert(imfs[0])
plt.plot(np.real(h), np.imag(h))
plt.xlim(-2,2)
plt.ylim(-2,2)

omega = np.unwrap(np.angle(h))
f_inst = np.diff(omega)
plt.figure()
plt.plot(t[1:], f_inst)


# In[Hilbert spectral analisys]


# Compute Hilbert transform
h0 = hilbert(imfs[0])
plt.plot(np.real(h0), np.imag(h0))


h1 = hilbert(imfs[1])
plt.plot(np.real(h1), np.imag(h1))


h2 = hilbert(imfs[2])
plt.plot(np.real(h2), np.imag(h2))

plt.xlim(-1,1)
plt.ylim(-1,1)


# instantaneous phase, instantaneous frequency
omega_0 = np.unwrap(np.angle(h0))
f_inst_0 = np.diff(omega_0)

omega_1 = np.unwrap(np.angle(h1))
f_inst_1 = np.diff(omega_1)

omega_2 = np.unwrap(np.angle(h2))
f_inst_2 = np.diff(omega_2)

plt.figure()
plt.plot(t[1:], f_inst_0)
plt.plot(t[1:], f_inst_1)
plt.plot(t[1:], f_inst_2)




