#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

cma, ctr, ctr_err = np.loadtxt("../data/hor_ma.dat", skiprows=1, unpack=True)
sma, shit, shit_err = np.loadtxt("../data/hor_ma_sim.dat", skiprows=1, unpack=True)

afs = 20

plt.figure()

plt.errorbar(cma, ctr, yerr=ctr_err, fmt='o', label='Bench Data', color='b')
plt.errorbar(sma, shit, yerr=shit_err, fmt='o', label='Simulated Data', color='r')

plt.title('Horizontal Misalignment Studies', size=afs)
plt.xlim(-0.1, 4.0)
plt.xlabel('Coupling Distance of Scintillator & SiPM (mm)', size=afs)
plt.ylim(0, 2500)
plt.ylabel('Time Resolution (ps)', size=afs)

plt.legend(loc=1, numpoints=1)

plt.show()
