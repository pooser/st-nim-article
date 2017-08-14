#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

cma, ctr, ctr_err = np.loadtxt("../data/vert_ma_coarse.dat", skiprows=1, unpack=True)
fma, ftr, ftr_err = np.loadtxt("../data/vert_ma_fine.dat", skiprows=1, unpack=True)
sma, shit = np.loadtxt("../data/vert_ma_sim.dat", skiprows=1, unpack=True)
shit_err = np.sqrt(shit)

afs = 20

plt.figure()

plt.errorbar(cma, ctr, yerr=ctr_err, fmt='o', label='Coarse Bench Data', color='b')
plt.errorbar(fma, ftr, yerr=ftr_err, fmt='o', label='Fine Bench Data', color='g')
plt.errorbar(sma, shit, yerr=shit_err, fmt='o', label='Simulated Data', color='r')

plt.title('Vertical Misalignment Studies', size=afs)
plt.xlim(-4.0, 4.0)
plt.xlabel('Vertical Misalignment of SiPM (mm)', size=afs)
plt.ylim(0, 2500)
plt.ylabel('Time Resolution (ps)', size=afs)

plt.legend(loc=1, numpoints=1)

plt.show()
