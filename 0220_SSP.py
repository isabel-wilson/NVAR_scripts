# %%
# Load packages
import mne
import matplotlib
matplotlib.use("TkAgg")

# Function for plotting spectrum
def plot_spectrum(data): 
    fig = data.compute_psd(proj = True).plot(
            average=False,
            dB=False,
            picks="data",
            exclude="bads"
        )
    fig.axes[0].set_xlim(1, 80)
    fig.axes[1].set_xlim(1, 80)
    fig.axes[0].set_ylim(1, 100000)
    fig.axes[1].set_ylim(1, 100000)
    fig.axes[0].set_ylabel("log Power")
    fig.axes[1].set_ylabel("log Power")
    fig.axes[0].set_yscale('log')
    fig.axes[1].set_yscale('log')
    return fig


#%%

""""
File bank: 
C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif
C:/meg/NVAR_preprocessing/MEG/sub_NVAR008/251016/sub_NVAR008_251016_rest2_raw_tsss.fif
C:/meg/NVAR_preprocessing/MEG/sub_NVAR010/251027/sub_NVAR010_251027_rest1_raw_tsss.fif
C:/meg/NVAR_preprocessing/MEG/sub_NVAR011/251030/sub_NVAR011_251030_rest1_raw_tsss.fif
"""

custom_ssp_freq_low = 50
custom_ssp_freq_high = 53

file = "C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif"
raw = mne.io.read_raw_fif(file, preload = True)
print("Active flags now:",
      [p['active'] for p in raw.info['projs']])
#plot_spectrum(raw)


#%%
raw_filt = raw.copy().filter(l_freq=custom_ssp_freq_low, h_freq=custom_ssp_freq_high)
raw_projs = mne.compute_proj_raw(raw_filt, n_grad=6, n_mag=6)
mne.viz.plot_projs_topomap(raw_projs, colorbar=True, vlim="joint", info=raw.info)
raw.add_proj(raw_projs) # It seems necessary to remove three PCs for both gradiometers and magnetometers
raw.add_proj(raw_projs)
raw.apply_proj()
print("Active flags now:",
      [p['active'] for p in raw.info['projs']])
plot_spectrum(raw)


# %%
# Only a subset of channels are affected by the artifact, look at it closeup
file = "C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif"
raw = mne.io.read_raw_fif(file, preload = True)
fig = raw.compute_psd(proj = True).plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(40, 60)
fig.axes[1].set_xlim(40, 60)
fig.axes[0].set_ylim(1, 100000)
fig.axes[1].set_ylim(1, 100000)
fig.axes[0].set_ylabel("log Power")
fig.axes[1].set_ylabel("log Power")
fig.axes[0].set_yscale('log')
fig.axes[1].set_yscale('log')


# B
# %%
