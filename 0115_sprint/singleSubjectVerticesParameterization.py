#%%
import time
import tracemalloc

# PROCESSING VARIABLES #
start_time = time.time()
tracemalloc.start()
# END OF PROCESSING VARIABLES #

import os
import sys
import mne
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from fooof import FOOOF, Bands

#FUNCTIONS#
def plotPSD(freqDomain, powerDomain, range = [0, 250]):
    plt.title(f"Frequency Spectrum Example ({range[0]} Hz to {range[1]} Hz)")
    plt.plot(freqDomain, powerDomain)
    plt.xlim(range)
    plt.ylabel("Power")
    plt.xlabel("Frequency (Hz)")
    plt.savefig(f"frequencySpectrum{range[0]}Hz_{range[1]}Hz.png")


#END OF FUNCTIONS#

#CONSTANTS#
if len(sys.argv) > 1:
    subject = sys.argv[1]
else:
    raise Exception("No subject passed.")

project_path = 'C:/meg/NVAR_sprint_fooof/output/NVAR001_rest1/nosprint/'
folder_path = 'C:/meg/NVAR_sprint_fooof/input/'

bands = Bands({'delta' : [1, 4], 
               'theta' : [4, 7], 
               'alpha' : [8, 12], 
               'beta' : [15, 29]})
#END OF CONSTANTS#

#MAIN CODE#
os.chdir(project_path) # Set working directory
print(f"Current working directory: {os.getcwd()}")

freqDomain = np.array([f/4 for f in range(0,1001)]) # Frequency range [0,250] with steps of 0.25 Hz

parameterColNames = [
    'vertex', 'offset', 'exponent', 
    'delta_cf', 'delta_pw', 'delta_bw',
    'theta_cf', 'theta_pw', 'theta_bw',
    'alpha_cf', 'alpha_pw', 'alpha_bw',
    'beta_cf', 'beta_pw', 'beta_bw',
    'error', 'r_squared'
]

parameterDF = pd.DataFrame(columns=parameterColNames)

fname = folder_path + "sub_NVAR001_rest1_raw_tsss_beamformer_stc-lh.stc"
stc = mne.read_source_estimate(fname)

vertices = stc.data

print(vertices.shape)

for v, freqPower in enumerate(vertices):
    fm = FOOOF()
    fm.fit(freqDomain, freqPower, freq_range=[1.0,40.0])
    vertexDF = fm.to_df(bands).to_frame().T
    vertexDF['vertex'] = v + 1

    parameterDF = pd.concat([parameterDF, vertexDF], ignore_index=True)

    if (v+1)%100 == 0:
        elapsed_time = time.time() - start_time
        print(f"Vertex {v+1} | Elapsed time: {elapsed_time:.4f} seconds")

parameterDF.to_csv(f"{project_path}outputs/foof_parameterization_PSD_{subject}.csv", index=False, na_rep="NaN")


#END OF MAIN CODE#

#PROCESSING INFO#
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 10**6:.2f} MB")
print(f"Peak memory usage: {peak / 10**6:.2f} MB")

tracemalloc.stop()

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
#END OF PROCESSING INFO#
# %%
