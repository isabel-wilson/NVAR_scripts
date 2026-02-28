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
##### ERM PROJECTORS: TRY OUT DIFFERENT THINGS
# DON'T CHANGE THIS, THIS CORRESPONDS TO HIGHLIGHTED NOTES
empty_room_raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_erm_raw.fif", preload = True)
plot_spectrum(empty_room_raw) # Always with proj = True
empty_room_raw_filt = empty_room_raw.copy().filter(l_freq=40, h_freq=45)
empty_room_projs = mne.compute_proj_raw(empty_room_raw_filt, n_grad=3, n_mag=0)
mne.viz.plot_projs_topomap(empty_room_projs, colorbar=True, vlim="joint", info=empty_room_raw.info)

raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif", preload = True)
raw.add_proj(empty_room_projs)
raw.apply_proj()
raw.info["projs"]
plot_spectrum(raw)


#%%
##### REST: TRY OUT DIFFERENT THINGS

raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR010/251027/sub_NVAR010_251027_rest1_raw_tsss.fif", preload = True)
raw_filt = raw.copy().filter(l_freq=40, h_freq=45)
raw_projs = mne.compute_proj_raw(raw_filt, n_grad=3, n_mag=3)
raw.add_proj(raw_projs)
raw.apply_proj()
raw.info["projs"]
plot_spectrum(raw)


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


# %%

file = "C:/meg/NVAR_preprocessing/MEG/sub_NVAR010/251027/sub_NVAR010_251027_rest1_raw_tsss.fif"
raw = mne.io.read_raw_fif(file, preload = True)
fig = raw.compute_psd(proj = True).plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(0, 80)
fig.axes[1].set_xlim(0, 80)
fig.axes[0].set_ylim(1, 100000)
fig.axes[1].set_ylim(1, 100000)
fig.axes[0].set_ylabel("log Power")
fig.axes[1].set_ylabel("log Power")
fig.axes[0].set_yscale('log')
fig.axes[1].set_yscale('log')
#%%
# --- Custom SSPs ---

# if custom_ssps: 
#     try: 
#         for custom_ssp in custom_ssps: 
#             custom_ssp_freq_lowlim = custom_ssp[0]
#             custom_ssp_freq_highlim = custom_ssp[1]

#             print(f"→ Applying custom SSP to repair artifact at {custom_ssp_freq_lowlim} to {custom_ssp_freq_highlim} Hz")

#             raw_filt = raw.copy().filter(l_freq=custom_ssp_freq_low, h_freq=custom_ssp_freq_high)
#             custom_projs = mne.compute_proj_raw(raw_filt, n_grad=3, n_mag=3)
            
#             for i in [0, 3, 4]: # first grad PC, first mag PC
#                 raw.add_proj(custom_projs[i])
#                 raw_erm.add_proj(custom_projs[i])
#             raw.apply_proj()
#             raw_erm.apply_proj()

#             report.add_figure(fig, title = f"PSD after applying custom SSP at {custom_ssp_freq_lowlim} to {custom_ssp_freq_highlim} Hz")

#     except Exception as e: 
#         print(f"⚠️ Custom SSP computation failed: {e}")


# %%
import mne
stc = mne.read_source_estimate("C:/meg/0115_NVAR_sprint_fooof/output/NVAR001_rest2/reformatted_stc/alpha")
stc.plot(
    subject = "sub_NVAR001", 
    subjects_dir = "C:/meg/0115_NVAR_sprint_fooof/MRI/freesurfer", 
    background = "w"
)

# %%
