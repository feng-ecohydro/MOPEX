import numpy as np
import os
import matplotlib.pyplot as plt

dir_path = '/Users/xuefeng/Documents/workspace/MOPEX/'
os.chdir(dir_path)

fh = open('./Basin_characteristics/Basin_indices.txt','r')
indices = fh.readlines()
fh.close() 

fh = open('./Basin_characteristics/Vegetation/IGBPTABP.438','r')
landcover = fh.readlines()
fh.close() 

# Initialize variable containers
di = np.zeros(len(indices[1:]))
et_ratio = np.zeros_like(di)
devB = np.zeros_like(di)
fsnow = np.zeros_like(di)
Tavg = np.zeros_like(di)

# Append variables into containers
for i, line in enumerate(indices[1:]): 
    _, d, et, dB, fs, Ta = line.split(',')
    di[i], et_ratio[i], devB[i], fsnow[i], Tavg[i] = float(d), float(et), float(dB), float(fs), float(Ta)

# Can be repeat for landcover types
fcrop = np.zeros(len(landcover))
furban = np.zeros_like(fcrop)
fmosaic = np.zeros_like(fcrop)
for i, line in enumerate(landcover): 
    ls = line.split()    
    fcrop[i], furban[i], fmosaic[i] = ls[12], ls[13], ls[14]

# Define Budyko function
def budyko(di):
    return np.sqrt(di*np.tanh(1.0/di)*(1.0 - np.exp(-di)))

''' plotting '''

# Reproduce Berghuijs Figure 1 
iselect = fsnow > 0.15

plt.figure(figsize=(6,4))
plt.plot(di, et_ratio, 'o', ms=5, color='green', mec='white', mew=0.2)
plt.plot(di[iselect], et_ratio[iselect], 'o', ms=5, color='red', mec='white', mew=0.2)
plt.plot(np.arange(0,5,0.1), budyko(np.arange(0,5,0.1)), 'black', lw=1)
plt.xlabel('Dryness index')
plt.ylabel('Evaporative index')
plt.tight_layout()

plt.figure(figsize=(5,4))
plt.plot(fsnow, devB, 'o', ms=5, color='green', mec='white', mew=0.2)
plt.plot(fsnow[iselect], devB[iselect], 'o', ms=5, color='red', mec='white', mew=0.2)
plt.xlabel('Snow fraction')
plt.ylabel('Deviation from Budyko curve')
plt.tight_layout()
plt.show()
