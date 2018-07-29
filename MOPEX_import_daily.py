import numpy as np
import glob, os
import matplotlib.pyplot as plt

dir_path = '/Users/xuefeng/Documents/workspace/MOPEX/'

def get_daily_station_names():
    file_names = []
    os.chdir(dir_path+'Us_438_Daily')
    for f in glob.glob('*.dly'):
        file_names.append(f)
    return file_names

def get_station_data(station_name = '01048000.dly'):
    fname = dir_path + 'Us_438_Daily/'+ station_name
    with open(fname) as f:
        content = f.read().split('\r\n')
    
    # precip, pet, and stream all in units of mm 
    precip = np.zeros(len(content[:-1]))
    pet = np.zeros_like(precip)
    stream = np.zeros_like(precip)
    year = np.zeros_like(precip)
    month = np.zeros_like(year)
    date = np.zeros_like(year)
    Tmax = np.zeros_like(year)
    Tmin = np.zeros_like(year)
    for i, line in enumerate(content[:-1]):  
        year[i] = float(line[:4].strip())
        month[i] = float(line[4:6].strip())
        date[i] = float(line[6:8].strip())
        precip[i] = float(line[8:18].strip())
        pet[i] = float(line[18:28].strip())
        stream[i] = float(line[28:38].strip())
        Tmax[i] = float(line[38:48].strip())
        Tmin[i] = float(line[48:58].strip())
    return year, month, date, np.ma.masked_less(precip, 0), np.ma.masked_less(pet, 0), np.ma.masked_less(stream, 0), Tmax, Tmin

def find_climatology(precip, pet, month, normed=False):
    precip_clima = np.zeros(12)
    pet_clima = np.zeros_like(precip_clima)
    for m in range(1, 13): 
        im = np.where(month==m)[0]
        precip_clima[m-1] = np.nanmean(precip[im])
        pet_clima[m-1] = np.nanmean(pet[im])
    if normed: 
        precip_clima = precip_clima/np.nansum(precip_clima)
        pet_clima = pet_clima/np.nansum(pet_clima)
    return precip_clima, pet_clima

def budyko(di):
    return np.sqrt(di*np.tanh(1.0/di)*(1.0 - np.exp(-di)))

if __name__ == "__main__":
    
    # Retrieve a list of station names 
    file_names = get_daily_station_names()
    
    # Initializing variable containers 
    fsnow = np.zeros(len(file_names))
    di = np.zeros_like(fsnow)
    et_ratio = np.zeros_like(fsnow)
    devB = np.zeros_like(fsnow)
    Tavg = np.zeros_like(fsnow)
    
    for j, fname in enumerate(file_names): 
        print(j)
        year, month, date, precip, pet, stream, Tmax, Tmin = get_station_data(fname)
    
        # Obtain snow fraction for each station
        snowdays = np.where((Tmax+Tmin)/2.0 < 1.0)[0]
        fsnow[j] = np.sum(precip[snowdays])/np.sum(precip)
        Tavg[j] = np.mean(0.5*(Tmax+Tmin))
        
        # Obtain dryness index, evaporative index, and deviation from Budyko curve
        di[j] = np.nanmean(pet)/(np.nanmean(precip))
        et_ratio[j] = 1.0 - np.nanmean(stream)/np.nanmean(precip)
        devB[j] = (1.0 - et_ratio[j]) - (1.0 - budyko(di[j]))

    # Plot Berghuijs Figure 1a 
    iselect = fsnow > 0.15
    plt.figure(figsize=(6,4))
    plt.plot(di, et_ratio, 'o', ms=5, color='green', mec='white', mew=0.2)
    plt.plot(di[iselect], et_ratio[iselect], 'o', ms=5, color='red', mec='white', mew=0.2)
    plt.plot(np.arange(0,5,0.1), budyko(np.arange(0,5,0.1)), 'black', lw=1)
    plt.xlabel('Dryness index'); plt.ylabel('Evaporative index')
    plt.tight_layout()
    plt.show()
    