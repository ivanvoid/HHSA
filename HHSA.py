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
# import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import hilbert
plt.style.use('bmh')
np.random.seed(1615552020)

from EMD import EMD, plot_imfs, max_min_env

def plt_signal(signal, l, c):
    plt.plot(signal, c, label=l, linewidth=1)
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.xlim(0,1000)
    plt.ylim(-1.5,1.5)
    plt.legend(loc='upper right')

def init():
    N = 1000

    t = np.arange(0,N)
    signal1 = np.sin(t * 0.02)
    signal2 = np.sin(t * 0.08)
    noise = np.random.uniform(-0.5,0.5,N)

    spn = signal1+noise
    smn = signal1*noise
    sps = signal1 * signal2

    # plt_signal(signal1,'Signal')
    # plt_signal(noise, 'Gaussian white noise', 'g')
    # plt_signal(spn, 'Signal + Noise', 'k')
    # plt_signal(smn, 'Signal * Noise', 'k')

    return spn, smn, signal1


spn, smn, signal = init()



# In[ Power Spectral Density ]
dt = 0.01
nfft = 1024
plt.psd(spn, nfft, 1/dt, label='Signal + Noise', c='#FF8E40')
plt.psd(signal, nfft, 1/dt,label='Signal', ls=':',c='#9282FF')
plt.xscale('log')
plt.ylim(-64, 9)

plt.legend()

plt.figure()
plt.psd(smn, nfft, 1/dt, label='Signal * Noise',c='#FF8E40')
plt.psd(signal, nfft, 1/dt,label='Signal', ls=':', c='#9282FF')
plt.xscale('log')
plt.ylim(-64, 9)

plt.legend()


# In[ First IMF ]
# Data plot
fig, ax = plt.subplots(1,2)
ax[0].plot(signal, 'w-', label='data')
ax[0].grid(linestyle='--', color=([0.2,0.2,0.2]))


imfs = EMD(signal, 3)

# IMF plot
for i in range(len(imfs)):
    ax[1].plot(imfs[i], label=str(i))
ax[1].grid(linestyle='--', color=([0.2,0.2,0.2]))

plt.legend()


# In[ Second IMF ]
max_envs = []
for imf in imfs:
    max_env, _ = max_min_env(imf)
    max_envs += [max_env]

new_imfs = []
for env in max_envs:
    new_imfs += EMD(env, 3)


for imf in new_imfs:
    plt.plot(imf)
plt.grid(linestyle='--', color=([0.2,0.2,0.2]))


# In[ Inst freq for first IMF ]
inst_freq = []
for imf in imfs:
    h = hilbert(imf)
    omega = np.unwrap(np.angle(h))
    inst_freq += [np.diff(omega)]

plt.plot(inst_freq[0], imfs[0][:-1], '.')
plt.xlabel('Instant freq')
plt.ylabel('IMF')

# In[ 3D plotter ]
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

i = 0

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(np.arange(0,len(imfs[i])-1),
           inst_freq[i],
           imfs[i][:-1],
           marker='p')

ax.set_xlabel('Time')
ax.set_ylabel('Instant frequancy')
ax.set_zlabel('IMF')

# In[ FFT ]

T = 1.0 / 250.0
N = 1000

spn_fft = np.fft.fft(spn)
smn_fft = np.fft.fft(smn)

xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
plt.plot(xf, 2.0/N * np.abs(spn_fft[:N//2]))
plt.plot(xf, 2.0/N * np.abs(smn_fft[:N//2]))


# In[]
t = np.arange(0,len(signal))
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

cbar = fig.colorbar(im, ticks=[-1, 0, 1])
cbar.ax.set_yticklabels(['< -1', '0', '> 1'])

plt.colorbar()
plt.show()


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




