# %%
# Load packages
import mne
import matplotlib
matplotlib.use("TkAgg")

# Function for plotting spectrum
def plot_spectrum(data): 
    fig = data.compute_psd().plot(
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
# Load ERM and view
empty_room_raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_erm_raw.fif", preload = True)
empty_room_raw_filt = empty_room_raw.copy().filter(l_freq=40, h_freq=45)
empty_room_projs = mne.compute_proj_raw(empty_room_raw_filt, n_grad=4, n_mag=4)
mne.viz.plot_projs_topomap(empty_room_projs, colorbar=True, vlim="joint", info=empty_room_raw.info)



file = "C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif"
raw = mne.io.read_raw_fif(file, preload = True)
raw.filter(l_freq=40, h_freq=45).add_proj(empty_room_projs)
raw.apply_proj()
plot_spectrum(raw)



# %%
# Load raw and view
raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif", preload = True)
plot_spectrum(raw)

#%%
# Apply projectors; note that adding only the first PC (or only magnetometers, or only 3rd PC in the case where that's the one with the appropriate topography...) makes no difference
raw1 = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif", preload = True)

raw1_filt = raw1.copy().filter(l_freq=42, h_freq=45)
raw1_projs = mne.compute_proj_raw(raw1_filt, n_grad=3, n_mag=3)

raw2 = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest2_raw_tsss.fif", preload = True)
raw2.add_proj(raw1_projs)
raw2.apply_proj()

# View spectrum; note that adding the argument proj = True to compute_psd() makes no difference
plot_spectrum(raw2)




#%%
raw.del_proj() 
copy = raw.copy()
copy.add_proj(empty_room_projs)

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

plot_spectrum(copy)

#%%
raw.add_proj(empty_room_projs).apply_proj()  
print("Applied SSP. Active flags now:",
      [p['active'] for p in raw.info['projs']])
plot_spectrum(raw)
# %%

# %%
common = sorted(set(empty_room_raw.ch_names) & set(raw.ch_names))
print("ERM channels:", len(empty_room_raw.ch_names))
print("REST channels:", len(raw.ch_names))
print("Common:", len(common))

# %%
list1= empty_room_raw.ch_names
list2 = raw.ch_names
diff1 = [x for x in list1 if x not in list2]

# Items in list2 not in list1
diff2 = [x for x in list2 if x not in list1]

# Symmetric difference (items not shared)
diff_all = list(set(list1) ^ set(list2))

print(diff1)  # ['apple']
print(diff2)  # ['date']
print(diff_all)  # ['apple', 'date']


#%%
################################################################
################################################################
# Load packages
import mne
import matplotlib
matplotlib.use("TkAgg")

# Function for plotting spectrum
def plot_spectrum(data): 
    fig = data.compute_psd().plot(
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


# Apply projectors; note that adding only the first PC (or only magnetometers, or only 3rd PC in the case where that's the one with the appropriate topography...) makes no difference
raw1 = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif", preload = True)

raw1_filt = raw1.copy().filter(l_freq=42, h_freq=45)
raw1_projs = mne.compute_proj_raw(raw1_filt, n_grad=3, n_mag=3)

raw2 = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest2_raw_tsss.fif", preload = True)
raw2.add_proj(raw1_projs)
raw2.apply_proj()

# View spectrum; note that adding the argument proj = True to compute_psd() makes no difference
plot_spectrum(raw2)

