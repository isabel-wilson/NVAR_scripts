#%%

"""
---------Overview--------------------------------------------------
Input: Beamformed stcs and src (i.e., output of generic_taskfree_MEGIN.py), atlas warped to subject

* define name of folder for outputs

subject = "subject"
* load atlas 
sessions = [sessions]
For session in sessions: 
    For run in [run1, run2]:
        * load files
        1. Parcellation -> PCA -> extract multiseries
        For series in multiseries: 
            2. SPRINT
            3. fooof, save output
            * save output with filename subject_session_run_seriesnum.txt

Output: fgs[0].get_params('peak_params') to text file


---------Before this script-----------------------------------------
Before running this script, run this on MRI data on Linux1: 
1. Download Schaefer atlas
https://github.com/ThomasYeoLab/CBIG/blob/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/FreeSurfer5.3/fsaverage/label/rh.Schaefer2018_200Parcels_17Networks_order.annot

2. Project to native space
SUBJECTS_DIR=/mnt/c/meg/NVAR_sprint_fooof/MRI/freesurfer
subjects=("sub_NVAR001")
for subject in "${subjects[@]}"; do
  for hemi in lh rh; do
    mri_surf2surf --srcsubject fsaverage \
      --trgsubject $subject \
      --hemi $hemi \
      --sval-annot /mnt/c/meg/NVAR_sprint_fooof/$hemi.Schaefer2018_200Parcels_17Networks_order.annot \
      --tval $SUBJECTS_DIR/$subject/label/$hemi.Schaefer2018_200.annot
  done
done

"""

#---------Load packages-----------------------------------------
from math import floor
from statistics import median
from itertools import compress
import numpy as np
import fooof
from fooof.data import FOOOFResults
from fooof.sim.gen import gen_periodic
from fooof.objs.utils import combine_fooofs
from copy import deepcopy
import mne
import SPRiNT_py as sprint

#---------User input--------------------------------------------

subject = "sub_NVAR010"
sessions = ["251027"]
base_path = "C:/meg/NVAR"

# Hyperparameters for SPRiNT:
# Below are defaults, except for the following changes (recommended by AW): 
opt = {
    "sfreq": 1000,  # Input sampling rate # CHANGED
    "WinLength": 4,  # STFT window length # CHANGED
    "WinOverlap": 50,  # Overlap between sliding windows (in %)
    "WinAverage": 5, # Number of overlapping windows being averaged
    "rmoutliers": 1, # Apply peak post-processing
    "maxTime": 6, # Maximum distance of nearby peaks in time (in n windows)
    "maxFreq": 2.5, # Maximum distance of nearby peaks in frequency (in Hz)
    "minNear": 3, # Minimum number of similar peaks nearby (using above bounds)
    }

#---------Load labels (from atlas) for this subject ------------

# Convert Schaefer2018_200.annot to labels
labels = mne.read_labels_from_annot(
    subject = subject,
    hemi = "both",
    parc = "Schaefer2018_200", 
    subjects_dir = base_path + "/MRI/freesurfer"
    )

#---------Begin loop----------------------------------------------

for session in sessions: 
    for run in ["rest1", "rest2"]: 

#---------Parcellation -> extract first PC-----------------------
        
        # Define paths to stcs and src, then load files
        stcs_path = base_path + "/derivatives/" + subject + "/" + session + "/beamformer/stc/" + subject + "_" + run + "_raw_tsss_beamformer_stc"
        src_path = base_path + "/derivatives/" + subject + "/" + session + "/sub_NVAR010_rest1_raw_tsss_src.fif"
        stcs = mne.read_source_estimate(stcs_path)
        src = mne.read_source_spaces(src_path)
        
        # Extract 202 timeseries
        multiseries = mne.extract_label_time_course(stcs = stcs, src = src, labels = labels, mode = "pca_flip")

#---------Loop through each series--------------------------

        for series in multiseries: 
            current_series = np.array([series])

#---------Run SPRiNT----------------------------------------

            output = sprint.SPRiNT_stft_py(current_series, opt) #TODO: need to save sprint output

#---------Run fooof----------------------------------------

            fg = fooof.FOOOFGroup(peak_width_limits=[2, 6],
                min_peak_height=0.5, max_n_peaks = 3)
            fgs = fooof.fit_fooof_3d(fg, output['freqs'], output['TF'], freq_range=[1, 40])

            #TODO: decide how to save this
            #TODO: decide how to save files in scratch


# Grab time series for vertex 0, which we'll use as the test
#F = stc.data[[0]]

# expects a numpy array
#output = SPRiNT_stft_py(F,opt)

# run fooof across channels and time
# Only issue: Does not use previous window's exponent estimate, haven't seen
# discrepancies yet (...)
# fg = power spectrum fit
#fg = fooof.FOOOFGroup(peak_width_limits=[2, 6],
 #   min_peak_height=0.5, max_n_peaks = 3)
#fgs = fooof.fit_fooof_3d(fg, output['freqs'], output['TF'], freq_range=[1, 40])

#print(fgs[0].get_params('peak_params'))
#with open(path + "output.txt", 'w') as file:
#    file.write(str(fgs[0].get_params('peak_params')))

# Optionally, you can remove outliers
# Set value in range(n) to num channels
#fgs = [SPRiNT_remove_outliers(fgs[i], output['ts'], opt) for i in range(1)]
# after removing outliers
#print(fgs[0].get_params('peak_params'))

# %%
