import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import random
import datetime
import h5py


fontsize=13


INPUT_PATH_BKG = './Z_5D_DATA/Zmumu_lepFilter_13TeV/'
INPUT_PATH_SIG = './Z_5D_DATA/Zprime_lepFilter_13TeV/M300/'
FILE_ID_BKG = 'Zmumu_13TeV_20PU_'
FILE_ID_SIG = 'Zprime_lepFilter_300GeV_13TeV_'

seed=datetime.datetime.now().microsecond+datetime.datetime.now().second+datetime.datetime.now().minute
np.random.seed(seed)

#random integer to select Zprime file between 0 and 9 (10 input files)
index_sig = np.arange(300)
index_sig = np.delete(index_sig,133,0)
np.random.shuffle(index_sig)
#random integer to select Zmumu file between 0 and 999 (1000 input files)
index_bkg = np.arange(1000)
np.random.shuffle(index_bkg)

N_Sig = 240000
N_Bkg = 1600000
nbins = 50

HLF_REF = np.array([])
HLF_name = ''
i=0
for v_i in index_bkg:
    f = h5py.File(INPUT_PATH_BKG + FILE_ID_BKG + str(v_i) + '.h5')
    hlf = np.array(f.get('HLF'))
    #print(hlf.shape)
    hlf_names = f.get('HLF_names')
    if not hlf_names:
        continue
    #select the column with px1, pz1, px2, py2, pz2
    cols = [0, 1, 7, 8, 9, 30]
    if i==0:
        HLF_REF=hlf[:, cols]
        i=i+1
    else:
        HLF_REF=np.concatenate((HLF_REF, hlf[:, cols]), axis=0)
    f.close()
    #print(HLF_REF.shape)
    if HLF_REF.shape[0]>=N_Bkg:
        HLF_REF = HLF_REF[:N_Bkg, :]
        break
print('HLF_REF+BKG shape')
print(HLF_REF.shape)

HLF_SIG = np.array([])
HLF_SIG_name = ''
i=0
for u_i in index_sig:
    f = h5py.File(INPUT_PATH_SIG + FILE_ID_SIG + str(u_i) + '.h5')
    hlf = np.array(f.get('HLF'))
    hlf_names = f.get('HLF_names')
    if not hlf_names:
        continue
    #select the column with px1, pz1, px2, py2, pz2
    cols = [0, 1, 7, 8, 9, 30]
    if i==0:
        HLF_SIG=hlf[:, cols]
        i=i+1
    else:
        HLF_SIG=np.concatenate((HLF_SIG, hlf[:, cols]), axis=0)
    f.close()
    if HLF_SIG.shape[0]>=N_Sig :
        HLF_SIG=HLF_SIG[:N_Sig, :]
        break
print('HLF_SIG shape')
print(HLF_SIG.shape)


feature = np.concatenate((HLF_REF, HLF_SIG), axis=0)
# feature = HLF_REF

#5D features construction (feature columns: [lep1px, lep1pz, lep2px, lep2py, lep2pz] )
p1 = np.sqrt(np.multiply(feature[:, 0], feature[:, 0])+np.multiply(feature[:, 1], feature[:, 1]))
pt1 = feature[:, 0]
pt2 = np.sqrt(np.multiply(feature[:, 2], feature[:, 2])+np.multiply(feature[:, 3], feature[:, 3]))
p2 = np.sqrt(np.multiply(pt2, pt2)+np.multiply(feature[:, 4], feature[:, 4]))
eta1 = np.arctanh(np.divide(feature[:, 1], p1))
eta2 = np.arctanh(np.divide(feature[:, 4], p2))
phi1 = np.arccos(np.divide(feature[:, 0], pt1))
phi2 = np.sign(feature[:, 3])*np.arccos(np.divide(feature[:, 2], pt2))+np.pi*(1-np.sign(feature[:, 3]))
delta_phi = phi2 - phi1
Zmass = feature[:, 5]
pt1 = np.expand_dims(pt1, axis=1)
pt2 = np.expand_dims(pt2, axis=1)
eta1 = np.expand_dims(eta1, axis=1)
eta2 = np.expand_dims(eta2, axis=1)
delta_phi = np.expand_dims(delta_phi, axis=1)
Zmass = np.expand_dims(Zmass, axis=1)

feature = np.concatenate((pt1, pt2), axis=1)
feature = np.concatenate((feature, eta1), axis=1)
feature = np.concatenate((feature, eta2), axis=1)
feature = np.concatenate((feature, delta_phi), axis=1)
feature = np.concatenate((feature, Zmass), axis=1)
print('final_features shape ')
print(feature.shape)

background = feature[:N_Bkg,:]
signal = feature[N_Bkg:N_Bkg+N_Sig,:]

"""
#standardize dataset
for j in range(feature.shape[1]):
    vec = feature[:, j]
    mean = np.mean(vec)
    std = np.std(vec)
    if np.min(vec) < 0:
        vec = vec- mean
        vec = vec *1./ std
    elif np.max(vec) > 1.0:# Assume data is exponential -- just set mean to 1.
        vec = vec *1./ mean
    feature[:, j] = vec
"""





plt.rc('text', usetex=True)
plt.rc('font', family='serif')

pt_bins_bkg = np.concatenate((np.arange(0,250,15), np.arange(250,500,50)), axis=0)
pt_bins_bkg = np.concatenate((pt_bins_bkg, np.arange(500,1000,100)), axis=0)
pt_bins_sig = np.concatenate((np.arange(0,400,15), np.arange(400,600,50)), axis=0)
pt_bins_sig = np.concatenate((pt_bins_sig, np.arange(600,1000,100)), axis=0)
mass_bins_bkg = np.concatenate((np.arange(0,250,10), np.arange(250,500,50)), axis=0)
mass_bins_bkg = np.concatenate((mass_bins_bkg, np.arange(500,1000,100)), axis=0)
mass_bins_sig = np.concatenate((np.arange(0,350,10), np.arange(350,500,50)), axis=0)
mass_bins_sig = np.concatenate((mass_bins_sig, np.arange(500,1000,100)), axis=0)
#mass_bins_sig = np.concatenate((np.arange(0,200,20), np.arange(200,350,10)), axis=0)
#mass_bins_sig = np.concatenate((mass_bins_sig, np.arange(350,700,50)), axis=0)
#mass_bins_sig = np.concatenate((mass_bins_sig, np.arange(700,1000,100)), axis=0)

fig = plt.figure(figsize=(13, 18))
plt.clf()
fig.clf()

plt.subplot(3,2,1)
plt.title('$p_{T,1}$ distribution', fontsize=fontsize)
plt.xlabel('$p_{T,1}$ [GeV/c]', fontsize=fontsize)
plt.ylabel('Density', fontsize=fontsize)
plt.yscale('log')
plt.hist(background[:,0], bins=pt_bins_bkg, histtype='step', linewidth=2, density=True, label='Background')
plt.hist(signal[:,0], bins=pt_bins_sig, histtype='step', linewidth=2, density=True, label='Signal')
plt.legend(fontsize=fontsize)

plt.subplot(3,2,2)
plt.title('$p_{T,2}$ distribution', fontsize=fontsize)
plt.xlabel('$p_{T,2}$ [GeV/c]', fontsize=fontsize)
plt.ylabel('Density', fontsize=fontsize)
plt.yscale('log')
plt.hist(background[:,1], bins=pt_bins_bkg, histtype='step', linewidth=2, density=True, label='Background')
plt.hist(signal[:,1], bins=pt_bins_sig, histtype='step', linewidth=2, density=True, label='Signal')
plt.legend(fontsize=fontsize)

plt.subplot(3,2,3)
plt.title('$\eta_{1}$ distribution', fontsize=fontsize)
plt.xlabel('$\eta_{1}$', fontsize=fontsize)
plt.ylabel('Density', fontsize=fontsize)
plt.hist(background[:,2], bins=nbins, histtype='step', linewidth=2, density=True, label='Background')
plt.hist(signal[:,2], bins=nbins, histtype='step', linewidth=2, density=True, label='Signal')
plt.legend(fontsize=fontsize)

plt.subplot(3,2,4)
plt.title('$\eta_{2}$ distribution', fontsize=fontsize)
plt.xlabel('$\eta_{2}$', fontsize=fontsize)
plt.ylabel('Density', fontsize=fontsize)
plt.hist(background[:,3], bins=nbins, histtype='step', linewidth=2, density=True, label='Background')
plt.hist(signal[:,3], bins=nbins, histtype='step', linewidth=2, density=True, label='Signal')
plt.legend(fontsize=fontsize)

plt.subplot(3,2,5)
plt.title('$\Delta \phi$ distribution', fontsize=fontsize)
plt.xlabel('$\Delta \phi$ [rad]', fontsize=fontsize)
plt.ylabel('Density', fontsize=fontsize)
plt.hist(background[:,4], bins=nbins, histtype='step', linewidth=2, density=True, label='Background')
plt.hist(signal[:,4], bins=nbins, histtype='step', linewidth=2, density=True, label='Signal')
plt.legend(fontsize=fontsize)

plt.subplot(3,2,6)
plt.title('$M_{Z}$ distribution', fontsize=fontsize)
plt.xlabel('$M_{Z}$ [GeV/c$^2$]', fontsize=fontsize)
plt.ylabel('Density', fontsize=fontsize)
plt.yscale('log')
plt.hist(background[:,5], bins=mass_bins_bkg, histtype='step', linewidth=2, density=True, label='Background')
plt.hist(signal[:,5], bins=mass_bins_sig, histtype='step', linewidth=2, density=True, label='Signal')
plt.legend(fontsize=fontsize)

fig.subplots_adjust(left = 0.05,right = 0.95,bottom = 0.035,top = 0.975)
fig.savefig('./Python/Z/features_Zmumu_Zprime.pdf')
plt.clf()
fig.clf()
