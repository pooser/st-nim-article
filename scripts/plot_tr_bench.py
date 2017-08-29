#!/usr/bin/python

import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import pylab as pyl

# Setup LaTeX environment
rc('text', usetex=True)

# Define constants
num_pad = 30
num_pos = 12
fs = 20 
xmin = 0
xmax = 60
ymin = 225
ymax = 475
sob = 39.5
xhw = 0.5

# Define font dictionary
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 20}

# Acquire the data
gbar, gzpos, gtr, gtr_err = np.loadtxt("../data/time_res_bench.dat", skiprows=1, unpack=True);

# Orgainze the data
bar = np.split(gbar, num_pad)
zpos = np.split(gzpos, num_pad)
tr = np.split(gtr, num_pad)
tr_err = np.split(gtr_err, num_pad)

# Calculate the weighted average and the associated error for each source position and all 30 paddles
sig2 = np.square(tr_err)
w = 1. / sig2
xw = tr * w
mu = np.array([])
var = np.array([])
for i in range(0, num_pos):
    mu = np.append(mu, np.sum(xw[:,i]) / np.sum(w[:,i]))
    var = np.append(var, np.sqrt(1. / np.sum(w[:,i])))

# Calculate the wieghted average of all source locations using th wieghted averages calculated above
mu_sig2 = np.square(var)
mu_w = 1. / mu_sig2
mu_xw = mu * mu_w
total_mu = np.sum(mu_xw) / np.sum(mu_w)
total_mu_var = np.sqrt(1. / np.sum(mu_w))
total_mu_min = total_mu - total_mu_var
total_mu_max = total_mu + total_mu_var

# Overlay plot
plt.figure()
for i in range(0, 30):
    plt.errorbar(zpos[i], tr[i], yerr=tr_err[i], fmt='o')
pyl.fill([sob, xmax, xmax, sob], [ymin, ymin, ymax, ymax], 'g', alpha=0.2, edgecolor='g')
plt.xlabel("Distance of Source from SiPM (cm)", fontdict=font)
plt.ylabel("Time Resolution (ps)", fontdict=font)
plt.title("Start Counter Bench Performance", fontdict=font)
plt.text(41, 425, "Nose Region", fontdict=font, color='darkred')
plt.ylim(ymin, ymax)
plt.xlim(xmin, xmax)
plt.show()

# Weighted average summary plot
#plt.figure()
#plt.errorbar(zpos[0], mu, yerr=var, fmt='o', label=r'$\sigma_{avg}^{all}$')
#pyl.fill([sob, xmax, xmax, sob], [ymin, ymin, ymax, ymax], 'g', alpha=0.2, edgecolor='g')
#plt.xlabel("Distance of Source from SiPM (cm)", fontdict=font)
#plt.ylabel("Time Resolution (ps)", fontdict=font)
#plt.title("Weighted Average of ST Performance", fontdict=font)
#plt.text(41, 425, "Nose Region", fontdict=font, color='darkred')
#plt.axhline(y=total_mu, color='r', linestyle='--',
#            label=r'$\sigma_{avg} = %d \pm %1.1f\ ps$'%(total_mu, total_mu_var))
#pyl.fill([xmin, xmax, xmax, xmin], [total_mu_min, total_mu_min, total_mu_max, total_mu_max], 'r', alpha=0.2, edgecolor='r')
#plt.legend(loc=2)
#plt.ylim(ymin, ymax)
#plt.xlim(xmin, xmax)
#plt.show()

# Weighted average summary plot v2
ntr = np.multiply(1., tr)
ntr_err = np.multiply(1., tr_err)
plt.figure()
plt.xlabel("Distance of Source from SiPM (cm)", fontdict=font)
plt.ylabel("Time Resolution (ps)", fontdict=font)
plt.title("Weighted Average ST Bench Performance", fontdict=font)
plt.text(41, 425, "Nose Region", fontdict=font, color='darkred')
for i in range(0, 12):
    if i < 11:
        pyl.fill([zpos[0][i] - xhw, zpos[0][i] + xhw, zpos[0][i] + xhw, zpos[0][i] - xhw],
                 [ntr[:,i].min() - ntr_err[:,i][ntr[:,i].argmin()], ntr[:,i].min() - ntr_err[:,i][ntr[:,i].argmin()], ntr[:,i].max() + ntr_err[:,i][ntr[:,i].argmax()], ntr[:,i].max() + ntr_err[:,i][ntr[:,i].argmax()]], 
                 'b', alpha=0.2, edgecolor='b')
    if i == 11:
        pyl.fill([zpos[0][i] - xhw, zpos[0][i] + xhw, zpos[0][i] + xhw, zpos[0][i] - xhw],
                 [ntr[:,i].min() - ntr_err[:,i][ntr[:,i].argmin()], ntr[:,i].min() - ntr_err[:,i][ntr[:,i].argmin()], ntr[:,i].max() + ntr_err[:,i][ntr[:,i].argmax()], ntr[:,i].max() + ntr_err[:,i][ntr[:,i].argmax()]], 
                 'b', alpha=0.2, edgecolor='b', label='Relative Spread of Time Resolutions')
plt.errorbar(zpos[0], mu, yerr=var, fmt='o', label='Weighted Avg. of Time Resolutions')
pyl.fill([sob, xmax, xmax, sob], [ymin, ymin, ymax, ymax], 'g', alpha=0.2, edgecolor='g')
plt.axhline(y=total_mu, color='r', linestyle='--',
            label=r'$\sigma_{avg} = %d \pm %1.1f\ ps$'%(total_mu, total_mu_var))
pyl.fill([xmin, xmax, xmax, xmin], [total_mu_min, total_mu_min, total_mu_max, total_mu_max], 'r', alpha=0.2, edgecolor='r')
plt.legend(loc=3, numpoints=1)         
plt.ylim(ymin, ymax)
plt.xlim(xmin, xmax)
plt.show()

# Individual paddle summary plot
plt.figure()
nw = 1. / ntr_err**2.
nxw = ntr*nw
nmu = np.array([])
nvar = np.array([])
pad = np.array([])
tr_min = np.array([])
tr_max = np.array([])
tr_avg = np.array([])
tr_min_err = np.array([])
tr_max_err = np.array([])
tr_avg_err = np.array([])
for i in range(0, 30):
    pad = np.append(pad, i+1)
    nmu = np.append(nmu, np.sum(nxw[i]) / np.sum(nw[i]))
    nvar = np.append(nvar, np.sqrt(1. / np.sum(nw[i])))
    tr_min = np.append(tr_min, ntr[i].min())
    tr_min_err = np.append(tr_min_err, ntr_err[i][ntr[i].argmin()])
    tr_max = np.append(tr_max, ntr[i].max())
    tr_max_err = np.append(tr_max_err, ntr_err[i][ntr[i].argmax()])
    plt.errorbar(pad[i], tr_min[i], yerr=tr_min_err[i], color='g', fmt='o', label='_nolegend_')
    plt.errorbar(pad[i], ntr[i].max(), yerr=ntr_err[i][ntr[i].argmax()], color='r', fmt='o', label='_nolegend_')
    plt.errorbar(pad[i], nmu[i], yerr=nvar[i], color='b', fmt='o', label='_nolegend_')
trmin_w = 1. / tr_min_err**2.0
trmin_xw = tr_min * trmin_w
trmin_mu = np.sum(trmin_xw) / np.sum(trmin_w)
trmin_var = np.sqrt(1. / np.sum(trmin_w))
trmax_w = 1. / tr_max_err**2.0
trmax_xw = tr_max * trmax_w
trmax_mu = np.sum(trmax_xw) / np.sum(trmax_w)
trmax_var = np.sqrt(1. / np.sum(trmax_w))
nmu_w = 1. / nvar**2.0
nmu_xw = nmu*nmu_w
nmu_mu = np.sum(nmu_xw) / np.sum(nmu_w)
nmu_var = np.sqrt(1. / np.sum(nmu_w))
plt.axhline(y=trmax_mu, color='r', linestyle='--', 
            label=r'$\sigma_{avg}^{max} = %d \pm %1.1f\ ps$'%(trmax_mu, trmax_var))
pyl.fill([-1, 31, 31, -1], 
         [trmax_mu - trmax_var, trmax_mu - trmax_var, trmax_mu + trmax_var, trmax_mu + trmax_var],
         'r', alpha=0.2, edgecolor='r')
plt.axhline(y=nmu_mu, color='b', linestyle='--', 
            label=r'$\sigma_{avg}^{avg} = %d \pm %1.1f\ ps$'%(nmu_mu, nmu_var))
pyl.fill([-1, 31, 31, -1], 
         [nmu_mu - nmu_var, nmu_mu - nmu_var, nmu_mu + nmu_var, nmu_mu + nmu_var],
         'b', alpha=0.2, edgecolor='b')
plt.axhline(y=trmin_mu, color='g', linestyle='--', 
            label=r'$\sigma_{avg}^{min} = %d \pm %1.1f\ ps$'%(trmin_mu, trmin_var))
pyl.fill([-1, 31, 31, -1], 
         [trmin_mu - trmin_var, trmin_mu - trmin_var, trmin_mu + trmin_var, trmin_mu + trmin_var],
         'g', alpha=0.2, edgecolor='g')
plt.legend(loc=2)
plt.ylim(200, 500)
plt.xlim(-1, 31)
plt.xlabel("Paddle Number", fontdict=font)
plt.ylabel("Time Resolution (ps)", fontdict=font)
plt.title("Start Counter Bench Performance", fontdict=font)
plt.show()

# Box plot
#ntr = np.multiply(1., tr)
#plt.figure()
#plt.boxplot(ntr, labels=zpos[0])
#plt.ylim(ymin, ymax)
#plt.xlim(xmin, xmax)
#plt.show()
