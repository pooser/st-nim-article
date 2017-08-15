#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

sdis, shit, shit_err = np.loadtxt("../data/sim_simple_straight.dat", skiprows=1, unpack=True)
ndis, nhit, nhit_err = np.loadtxt("../data/sim_simple_nose.dat", skiprows=1, unpack=True)

afs = 20

plt.figure()

plt.errorbar(ndis, nhit, yerr=nhit_err, fmt='o', label='Nose Section', color='g')
plt.errorbar(sdis, shit, yerr=shit_err, fmt='o', label='Straight Section', color='b')

plt.title('Simplified Model', size=afs)
plt.xlim(0, 400)
plt.xlabel('Distance of Source From SiPM (mm)', size=afs)
plt.ylim(0, 1600)
plt.ylabel('Number of Hits in SiPM', size=afs)

plt.legend(loc=1, numpoints=1)

plt.show()
