#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

sdis, shit = np.loadtxt("../data/sim_simple_straight.dat", skiprows=1, unpack=True)
ndis, nhit = np.loadtxt("../data/sim_simple_nose.dat", skiprows=1, unpack=True)

shit_err = np.sqrt(shit)
nhit_err = np.sqrt(nhit)

afs = 20

plt.figure()

plt.errorbar(ndis, nhit, yerr=nhit_err, fmt='o', label='Nose Section', color='g')
plt.errorbar(sdis, shit, yerr=shit_err, fmt='o', label='Straight Section', color='b')

plt.title('Simplified Model', size=afs)
plt.xlim(0, 275)
plt.xlabel('Distance of Source From SiPM (cm)', size=afs)
plt.ylim(0, 1600)
plt.ylabel('Number of Hits in SiPM', size=afs)

plt.legend(loc=2, numpoints=1)

plt.show()
