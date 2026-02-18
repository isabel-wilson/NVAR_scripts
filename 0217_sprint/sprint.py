#%%
# Python SPRiNT
# Author: Luc Wilson (2023)

"""
Running this script runs sprint
Put inputs into this file (beginning in line ~200ish)

Default hyperparameters: 
opt = {
    "sfreq": 200, # Input sampling rate
    "WinLength": 1, # STFT window length
    "WinOverlap": 50, # Overlap between sliding windows (in %)
    "WinAverage": 5, # Number of overlapping windows being averaged
    "rmoutliers": 1, # Apply peak post-processing
    "maxTime": 6, # Maximum distance of nearby peaks in time (in n windows)
    "maxFreq": 2.5, # Maximum distance of nearby peaks in frequency (in Hz)
    "minNear": 3, # Minimum number of similar peaks nearby (using above bounds)
    }

"""
#----------------------------------------------------------
#------ Import packages -----------------------------------

from math import floor
from statistics import median
from itertools import compress
import numpy as np
import pandas as pd
import fooof
from fooof import Bands
from fooof.data import FOOOFResults
from fooof.sim.gen import gen_periodic
from fooof.sim.gen import gen_aperiodic
from fooof.objs.utils import combine_fooofs
from copy import deepcopy
import mne # Needed for user-specific part of script
import pickle as pkl

#----------------------------------------------------------
#------ Define functions ----------------------------------

# Takes in: beamformed data

# INPUT: 
# F should be a nxm numpy array
# where n is the number of channels, m is the number of samples
# opt should be a dictionary

# OUTPUT: 
# TF = time-frequency representation, dimensions (channels, time_windows (ts), frequency_bins (freqs))
# took the short-time fourier transform of overlapping windows
# freqs = frequency bins for TF
# ts = time windows for TF
def SPRiNT_stft_py(F, opt):
    ''' SPRiNT_stft_py: Compute a locally averaged short-time Fourier transform
    (for use in SPRiNT)

    Inputs
    F - Time series (nxm numpy array),
    where n is number of channels, m is number of samples
    opt - Model settings/hyperparameters (dict)

    Segments of this function were adapted from the Brainstorm software package:
    https://neuroimage.usc.edu/brainstorm
    Tadel et al. (2011)

    Author: Luc Wilson (2023)
    '''
    # Get sampling frequency
    n_chan = F.shape
    # print(n_chan)
    if not len(n_chan) > 1:
        n_sample = n_chan[0]
    else:
        n_sample = n_chan[1]

    sfreq = opt['sfreq']
    avgWin = opt['WinAverage']

    # Initialize returned values
    ind_good = 1  # index for kept data

    # WINDOWING
    Lwin = round(opt['WinLength'] * opt['sfreq'])  # n data points per window
    Loverlap = round(Lwin * opt["WinOverlap"] / 100)  # n data points in overlap

    # If window is too small
    Messages = []
    if Lwin < 50:
        print("Time window too small, please increase and run process again.")
        return
    # If window is bigger than the data
    elif Lwin > n_sample:
        Lwin = len(F[0])
        Lwin = Lwin - (Lwin % 2)  # Make sure the number of samples is even
        Loverlap = 0
        Nwin = 1
        print("Time window too large, using entire recording for spectrum.")
    # Else: there is at least one full time window
    else:
        Lwin = Lwin - (Lwin % 2)  # Make sure the number of samples is even
        Nwin = (n_sample - Loverlap) // (Lwin - Loverlap)

    # Positive frequency bins spanned by FFT
    FreqVector = sfreq / 2 * np.linspace(0, 1, round(Lwin / 2 + 1))
    # Determine hamming window shape/power
    Win = np.hanning(Lwin)
    WinNoisePowerGain = sum(Win**2)
    # Initialize STFT, time matrices
    ts = np.full((Nwin-(avgWin-1)),np.nan)
    if len(n_chan) > 1:
        TF = np.full((len(F), Nwin - (avgWin - 1), len(FreqVector)), np.nan)
        TFtmp = np.full((len(F), avgWin, len(FreqVector)), np.nan)
    else:
        TF = np.full((1, Nwin - (avgWin - 1), len(FreqVector)), np.nan)
        TFtmp = np.full((1, avgWin, len(FreqVector)), np.nan)
    # Calculate FFT for each window
    TFfull = np.zeros((len(F), Nwin, len(FreqVector)))
    for iWin in range(Nwin):
        # print(iWin)
        # Build indices
        iTimes = list(range((iWin)*(Lwin-Loverlap),Lwin+(iWin)*(Lwin-Loverlap)))
        center_time = floor(median(np.add(np.array(iTimes),1))-\
            (avgWin-1)/2*(Lwin-Loverlap))/200
        if len(n_chan) > 1:
            Fwin = F[:, iTimes]
            Fwin = Fwin- Fwin.mean(axis=1, keepdims=True)
        else:
            # print(iTimes)
            Fwin = F[iTimes]
            # print(Fwin)
            Fwin = Fwin - Fwin.mean()
        # Apply a Hann window to signal
        Fw = np.multiply(Fwin,Win)
        # Compute FFT
        Ffft = np.fft.fft(Fw, Lwin)
        if len(n_chan) > 1:
            TFwin = Ffft[:, :Lwin//2+1] * \
                np.sqrt(2 / (sfreq * WinNoisePowerGain))
            TFwin[:, [0, -1]] = TFwin[:, [0, -1]] / np.sqrt(2)
            # print(TFwin)
            TFwin = np.abs(TFwin)**2
            TFfull[:,iWin,:] = TFwin
            TFtmp[:, iWin % avgWin, :] = TFwin
            # print(iWin%avgWin)
        else:
            TFwin = Ffft[:Lwin//2+1] * np.sqrt(2 / (sfreq * WinNoisePowerGain))
            TFwin[[0, -1]] = TFwin[[0, -1]] / np.sqrt(2)
            # print(TFwin)
            TFwin = np.abs(TFwin)**2
            TFfull[:,iWin,:] = TFwin
            TFtmp[:, iWin % avgWin, :] = TFwin
        if np.isnan(TFtmp[-1, -1, -1]):
            pass
            # continue  # Do not record anything until transient is gone
        else:
            # Save STFTs for window
            TF[:, iWin - (avgWin - 1), :] = np.mean(TFtmp, axis=1)
            ts[iWin - (avgWin - 1)] = center_time
            # print(center_time)

    output = {
        "TF": TF,
        "freqs": FreqVector,
        "ts": ts,
        "options": opt
    }

    return output

def SPRiNT_remove_outliers(fooof_chan, ts, opt):
    ''' SPRiNT_remove_outliers: helper function to remove outlier peaks
    according to user-defined specifications

    Input
    fooof_chan - fooof model for a given channel (FOOOFObject)
    ts - sampled times (numpy array)
    opt - Model settings/hyperparameters (dict)

    Author: Luc Wilson (2023)
    '''
    n_peaks_changed = True
    peaks = fooof_chan.get_params('gaussian_params')
    n_peaks = len(peaks)
    npeak_bytime = fooof_chan.n_peaks_

    peaks_tmp = peaks
    n_peaks_tmp = n_peaks
    npeak_bytime_tmp = deepcopy(npeak_bytime)

    while n_peaks_changed:
        n_peaks_changed = False
        remove = [False for _ in range(n_peaks_tmp)]
        n_peaks_tmp2 = n_peaks_tmp

        for p in range(n_peaks_tmp):
            n_close = 0
            close_t = [(np.abs(peaks_tmp[p,3] - peaks_tmp[r,3])\
                <= opt['maxTime']) for r in range(n_peaks_tmp2)]
            close_f = [(np.abs(peaks_tmp[p,0] - peaks_tmp[r,0])\
                <= opt['maxFreq']) for r in range(n_peaks_tmp2)]

            for r in range(n_peaks_tmp2):
                if close_t[r] and close_f[r]:
                    n_close +=1 # had to flesh out to avoid bugs

            if n_close < (opt['minNear']+1): # fewer than min neighbors
                remove[p] = True # remove this peak
                npeak_bytime_tmp[int(peaks_tmp[p,3])] -= 1 # one less peak here
                n_peaks_tmp -= 1 # one less peak overall
                n_peaks_changed = True

        peaks_tmp = peaks_tmp[[not bln for bln in remove]]

    fg = list([])
    for t in range(len(ts)):
        tmp = fooof_chan.get_fooof(t)
        if npeak_bytime_tmp[t] != npeak_bytime[t]:
            if npeak_bytime_tmp[t] == 0:
                # all peaks at this time were removed
                gaus_pars = []
                pk_fit = gen_periodic(tmp.freqs, [])
                ap_pars = tmp._simple_ap_fit(tmp.freqs,tmp.power_spectrum)
                ap_fit = gen_aperiodic(tmp.freqs, ap_pars)
            else:
                # some peaks at this time were removed
                # finds the indices where time = t
                gaus_pars = peaks_tmp[np.where(peaks_tmp[:,3] == t)[0],:3]
                pk_fit = gen_periodic(tmp.freqs, np.ndarray.flatten(gaus_pars))
                ap_pars = tmp._simple_ap_fit(tmp.freqs,tmp.power_spectrum-pk_fit)
                ap_fit = gen_aperiodic(tmp.freqs, ap_pars)
            error = np.abs(tmp.power_spectrum - ap_fit - pk_fit).mean()
            r_squared = np.corrcoef(tmp.power_spectrum, ap_fit + pk_fit)[0][1]**2
            tmp.add_results(FOOOFResults(ap_pars,\
                tmp._create_peak_params(gaus_pars), r_squared, error, gaus_pars))
        fg.append(tmp)
    fg = combine_fooofs(fg)
    return fg

#----------------------------------------------------------
#------ User input ----------------------------------------

# Begin user-specific code
path = "C:/meg/NVAR/" #"/home/isw3/scratch/sprint/"
subject = "test"

#----------------------------------------------------------
#------ Run sprint and fooof ------------------------------

# Get data: Read stc files
# Files are beamformed stcs for each individual/session/scan
# Note that the data attribute of the stc has format n_vertices, n_times
# On Linux 1 they are listed with the format /home/nanolab/Documents/NVAR/derivatives/sub_NVAR008/251016/beamformer/stc
stc_file = path + "input/" + subject
print("Path to stc: " + stc_file)
stc = mne.read_source_estimate(stc_file)
print("stc loaded")
F = stc.lh_data[[0]]

# Set hyperparameters
# Below are defaults, with notes for changes: 
opt = {
    "sfreq": 500, # Input sampling rate 
    "WinLength": 4, # STFT window length
    "WinOverlap": 50, # Overlap between sliding windows (in %)
    "WinAverage": 5, # Number of overlapping windows being averaged
    "rmoutliers": 1, # Apply peak post-processing
    "maxTime": 6, # Maximum distance of nearby peaks in time (in n windows)
    "maxFreq": 2.5, # Maximum distance of nearby peaks in frequency (in Hz)
    "minNear": 3, # Minimum number of similar peaks nearby (using above bounds)
    }

bands = Bands({'delta' : [1, 4],
               'theta' : [4, 7],
               'alpha' : [8, 12],
               'beta' : [15, 29]})

print("parameters set")

# expects a numpy array
print("Running sprint:")
output = SPRiNT_stft_py(F, opt)
print("Done running sprint")

# Write to file
print("Writing sprint output to file:")
with open(f"{path}output/sprint_output.pkl", "wb") as file:
    pkl.dump(output["TF"], file)
print("Done writing sprint output to file")

# run fooof across channels and time
# Note in og code: "Only issue: Does not use previous window's exponent estimate, haven't seen discrepancies yet (...)"
# These params have been confirmed with AW
print("Running fooof:")
fg = fooof.FOOOFGroup(peak_width_limits=[2, 6], min_peak_height=0.5, max_n_peaks=3)
# second param is freq domain, third is power domain
fgs = fooof.fit_fooof_3d(fg, output['freqs'], output['TF'], freq_range=[1, 40])
print("Done running fooof")

# Write to file
# Each row in file will be a window
print("Writing fooof output to file:")
for i in range(len(fgs)): 
    df = fgs[i].to_df(bands)
    df.to_csv(f"{path}output/foof_{subject}_vertex_{str(i)}.csv", na_rep="NaN")
print("Done writing fooof output to file")

# %%
