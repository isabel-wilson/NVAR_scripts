#%% -----------------------------------------------------
# IMPORT PACKAGES

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re 
import pickle as pkl
import mne
import copy as copy
from pathlib import Path
import csv
import pickle

#%% -----------------------------------------------------
# SET UP

# Subject id
subject = "NVAR001"
run = "rest2"

# Folder names
session = subject + "_" + run
base_dir = "C:/meg/NVAR_sprint_fooof"
output_dir = os.path.join(base_dir, "output", session)
og_dir = os.path.join(output_dir, "og")
ref_dir = os.path.join(output_dir, "reformatted")
ref_stc_dir = os.path.join(output_dir, "reformatted_stc")
ref_stc_params_dir = os.path.join(output_dir, "reformatted_stc_params")
input_dir = os.path.join(base_dir, "input")

# File names, may be helpful later
stc_name = "sub_" + session + "_raw_tsss_beamformer_stc"
stc_path = os.path.join(input_dir, stc_name)
src_path = os.path.join(input_dir, "sub_" + session + "_raw_tsss_src.fif")
sprint_path = os.path.join(og_dir, "sprint_output.pkl")

#%% -----------------------------------------------------
# LOAD ORIGINAL STC

# Load stc for this subject
stc = mne.read_source_estimate(stc_path)



#%% -----------------------------------------------------
# REFORMAT FOOOF OUTPUT

# I coded sprint kind of incorrectly, where the output is appended with the vertex index rather than the vertex number itself. 
# (that's why in the output dir the vertices go 0, 1, ..., n even though we all know stc files could never)
# So here I have to work with vertex index. Output will be appended with actual vertex number
# such that the problem is fixed in the _reformatted stage

def reformat(csv_prefix):
    for time_window in range(55):
        rows = []

        for data_index in range(len(stc.data)):

            og_csv_path = f"{og_dir}/{csv_prefix}_vertex_{data_index}.csv"
            og_df = pd.read_csv(og_csv_path)

            row = og_df.iloc[time_window].copy()
            row['vertex_index'] = data_index
            rows.append(row)

        pd.DataFrame(rows).to_csv(f"{ref_dir}/{csv_prefix}_window_{time_window}.csv", index=False)

reformat("foof_" + stc_name)

#%% -----------------------------------------------------
# PARAMETERS INTO STC
# I want a [beta_pw, exponent, offset, model error] at each time window/csv

for keyword in ["beta_pw", "exponent", "offset", "error"]: 

    # Initialize array
    new_data = np.zeros(shape = (8196, 55))
    new_times = np.zeros(shape = (55, ))

    # Loop through time windows
    for window_num in range(55): 
        window_file = pd.read_csv(f"{ref_dir}/foof_{stc_name}_window_{window_num}.csv")
        
        measure = window_file[keyword].to_numpy().reshape(-1, 1)
        measure[np.isnan(measure)] = 0

        new_data[:, window_num] = measure[:, 0]
        new_times[window_num] = window_num

    # Write to stc
    new_stc = mne.SourceEstimate(
        data=new_data, 
        vertices=stc.vertices,
        tmin=0, 
        tstep=1
        )
    new_stc.save(os.path.join(ref_stc_params_dir, keyword), overwrite=True)

    # brain = new_stc.plot(
    #     subject='sub_' + subject, 
    #     subjects_dir="C:/meg/NVAR_sprint_fooof/MRI/freesurfer/", 
    #     initial_time=0, 
    #     hemi='both'
    # )




#%% -----------------------------------------------------
# PSD FROM SPRINT

# Read pickle
with open(sprint_path, "rb") as f:
    sprint_output = pickle.load(f)

"""
{'TF': array([[[3.31908108e-03, 1.02582303e-02, 8.88306617e-02, ...,
          9.70627037e-09, 1.11829197e-08, 5.25525509e-09],
         [2.96408614e-03, 1.69900910e-02, 7.49004008e-02, ...,
          7.25223534e-09, 5.75652586e-09, 2.79190429e-09],
         [9.34263580e-03, 3.87811856e-02, 1.28666873e-01, ...,
          2.81715080e-08, 1.46847533e-08, 8.24747301e-09],
         [1.95411091e-02, 9.29586804e-02, 2.41253203e-01, ...,
          2.65038759e-08, 1.45788630e-08, 1.04515533e-08]]],
       shape=(8196, 55, 2001)),
 'freqs': array([0.0000e+00, 2.5000e-01, 5.0000e-01, ..., 4.9950e+02, 4.9975e+02,
        5.0000e+02], shape=(2001,)),
 'ts': array([ 30.,  40.,  50.,  60.,  70.,  80.,  90., 100., 110., 120., 130.,
        140., 150., 160., 170., 180., 190., 200., 210., 220., 230., 240.,
        250., 260., 270., 280., 290., 300., 310., 320., 330., 340., 350.,
        360., 370., 380., 390., 400., 410., 420., 430., 440., 450., 460.,
        470., 480., 490., 500., 510., 520., 530., 540., 550., 560., 570.]),
 'options': {'sfreq': 1000,
  'WinLength': 4,
  'WinOverlap': 50,
  'WinAverage': 5,
  'rmoutliers': 1,
  'maxTime': 6,
  'maxFreq': 2.5,
  'minNear': 3}}

"""

# Plot one for each timepoint
# for NVAR001_rest1 sprint_output is the TF array directly; for the rest you need to extract
TF = sprint_output["TF"]
freqs = sprint_output["freqs"]
ts = sprint_output["ts"]
# Crop frequency width
TF_cropped = TF[:, :, :161]
freqs = freqs[:161]
# First take the mean
TF_wb_mean = TF_cropped.mean(axis=0)
# Take log
TF_log = np.log(TF_wb_mean)

plt.imshow(
    TF_log.T,
    aspect="auto",
    origin="lower",
    extent=[ts[0], ts[-1], freqs[0], freqs[-1]]
)
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Log power (a.u.)")
plt.title("SPRINT output")
plt.show()

#%% -----------------------------------------------------
# PSD FOR EACH TIME
colors = plt.cm.turbo(np.linspace(0, 1, 161))
# Loop through times
for i in range(len(TF_log)):
    plt.plot(TF_log[i], color=colors[i], alpha=0.6)
plt.xticks(np.arange(0, 161, 20), freqs[np.arange(0, 161, 20)])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Log power (a.u.)")
plt.title("SPRINT output \n colored by time window")

#%% -----------------------------------------------------
# CREATE INDIVIDUAL STCS
# One stc for each time window
# You should have 55 stcs, and each is PSD vs freq

# Do not log it
# Starts at 2 because I noticed during whitening the model fit worse there
# Ends at 161 because that's 40 Hz
TF_cropped = TF[:, :, 2:161]

for j in range(TF_cropped.shape[1]): 
    slice_j = TF_cropped[:, j, :]
    new_stc = mne.SourceEstimate(
        data = slice_j, 
        vertices = stc.vertices, 
        tmin = 0.5, 
        tstep = 0.25
    )
    new_stc.save(os.path.join(ref_stc_dir, str(j)), overwrite=True)

# Check: plot each one
#stc_check = mne.read_source_estimate(os.path.join(ref_stc_dir, str(49)))
#plt.plot(np.arange(0, 200), stc_check.data.mean(axis = 0))

#%% -----------------------------------------------------
# SUBTRACTION
# Do one window at a time
# input is stc in reformatted_stcs folder (psd, not yet logged) and window-formatted csv fooof output
# Output is _whitened.stc, saved in reformatted_stcs folder

# Frequency dimension: Goal is to match the dimension of the stc frequency array, which is:
freq_dim = freqs[2:161]

for window_num in range(55): 
    print(str(window_num))

    ##### Prep

    # Load files that you will need
    current_stc = os.path.join(ref_stc_dir, str(window_num))
    stc = mne.read_source_estimate(current_stc)
    current_csv = os.path.join(ref_dir, "foof_sub_" + session + "_raw_tsss_beamformer_stc_window_" + str(window_num) + ".csv")
    csv = pd.read_csv(current_csv)


    ##### PSD Model (exponential)

    # This is the list where you will put the model for each vertex
    rows = []

    # Get average offset and exponent for this subject (to be used for fixing bad values)
    average_exponent = np.nanmean(csv.iloc[:, 2])
    average_offset = np.nanmean(csv.iloc[:, 1])

    # Loop through rows of csv file
    for i in range(len(csv)): 
        
        # Collect values
        vertex = int(csv.iloc[i, 0])
        exponent = csv.iloc[i, 2]
        offset = csv.iloc[i, 1]

        # Make sure values look okay; if there are errors, replace with subject mean
        if type(exponent) != np.float64 or not np.isfinite(exponent): 
            print("error in exponent for subject " + subject + " vertex " + str(vertex) + ", setting to subject average")
            exponent = average_exponent
        if type(offset) != np.float64 or not np.isfinite(offset): 
            print("error in offset for subject " + subject + " vertex " + str(vertex) + ", setting to subject average")
            offset = average_offset

        # Compute exponential for this vertex
        # In linear space - not in log space
        exponential = 10**(offset - (np.log10(freq_dim))*exponent)
    #   print(exponential)
    #   print(freq_dim[0, 0])
    #   print(offset)
    #   print(exponent)

        # Add the exponential for this vertex to the "rows" list
        rows.append(exponential)

    # The final array of all exponentials for all vertices (cleaned up)
    model = np.array(rows).squeeze()

    ##### Subtraction

    # Whiten PSD: Subtract model PSD from real PSD
    # model: comes in not logged (linear)
    # stc data: comes in not logged (linear)
    # frequency is linear for both
    # subtraction happens in linear-linear space
    whitened_psd = stc.data - model

    # Create a plot for whitened PSD, and save it for review
    plt.figure()
    plt.plot(freq_dim, np.average(model.T, axis=1), label="Aperiodic fit", color="blue")
    plt.plot(stc.times, np.average(stc.data.T, axis=1), label="Original PSD", color="black")
    plt.plot(freq_dim, np.average(whitened_psd.T, axis=1), label="Whitened PSD", color="red")
    plt.ylabel("Power")
    plt.xlabel("Frequency")
    plt.legend()
    plt.title("Window " + str(window_num) + " detrending")
    plt.savefig(os.path.join(output_dir, "Images/Subtraction", str(window_num) + "_whitened.png"), dpi=300, bbox_inches="tight") 
    plt.close()

    # Convert the whitened psd to stc, then save it
    whitened_psd_stc = mne.SourceEstimate(
        data=whitened_psd,
        vertices=stc.vertices,
        tmin=0, 
        tstep=0.25
        )
    whitened_psd_stc.save(os.path.join(ref_stc_dir, str(window_num) + "_whitened"), overwrite=True)

#%% -----------------------------------------------------
# BREAK WHITENED STCS INTO FREQUENCY BANDS

bands = {'delta' : [1, 4], 'theta' : [4, 7], 'alpha' : [8, 12], 'beta' : [15, 29]}

window = 0
band = "delta"

low = bands[band][0]
high = bands[band][1]

stc = mne.read_source_estimate(os.path.join(ref_stc_dir, str(window_num) + "_whitened"))

trimmed_data = stc.data[:, (stc.times <= high) & (stc.times >= low)]
average_in_this_window = trimmed_data.mean(axis=1) # Compute average across all freqs
#new_times = stc.times[(stc.times <= 4) & (stc.times >= 1)]

new_stc = mne.SourceEstimate(
    data=average_in_this_window, 
    vertices=stc.vertices,
    tmin=0, 
    tstep=1
    )

new_stc.save(os.path.join(ref_stc_dir, band + "_" + str(window_num)), overwrite=True)



new_data = np.zeros(shape = (8196, 55))
new_times = np.zeros(shape = (55, ))

# Loop through time windows
for window_num in range(55): 
    window_file = pd.read_csv(f"{ref_dir}/foof_{stc_name}_window_{window_num}.csv")
    
    measure = window_file[keyword].to_numpy().reshape(-1, 1)
    measure[np.isnan(measure)] = 0

    new_data[:, window_num] = measure[:, 0]
    new_times[window_num] = window_num

#%% -----------------------------------------------------
# BUTTERFLY PLOTS


# Butterfly-plot
plt.plot(new_stc.times, new_stc.data.T)



