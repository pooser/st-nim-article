#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

ma, tr, tr_err = np.loadtxt("../data/vert_ma.dat", skiprows=1, unpack=True)
sma, shit, shit_err = np.loadtxt("../data/vert_ma_sim.dat", skiprows=1, unpack=True)

afs = 20

shit_max = np.amax(shit)
shit_max_idx = np.argmax(shit)
shit_max_err = shit_err[shit_max_idx]
conv_factor = np.sqrt(shit_max/shit)
tr_min = np.amin(tr)

sim_tr = conv_factor * tr_min
sim_tr_err = (np.sqrt(shit_max)/2. * shit**(-1.5) * shit_err) * tr_min

plt.figure()

plt.errorbar(ma, tr, yerr=tr_err, fmt='o', label='Bench Data', color='b')
plt.errorbar(sma, sim_tr, yerr=sim_tr_err, fmt='o', label='Simulated Data', color='r')

plt.title('Vertical Misalignment Studies', size=afs)
plt.xlim(-3.0, 3.0)
plt.xlabel('Vertical Misalignment of SiPM (mm)', size=afs)
plt.ylim(300, 550)
plt.ylabel('Time Resolution (ps)', size=afs)

plt.legend(loc=2, numpoints=1)

plt.show()
