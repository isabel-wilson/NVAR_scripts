# %%
import mne
import os
import matplotlib
matplotlib.use("TkAgg")  # or "Qt5Agg"
import matplotlib.pyplot as plt

empty_room_raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_erm_raw.fif", preload = True)
empty_room_raw.del_proj()
spectrum = empty_room_raw.compute_psd()
fig = spectrum.plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(1, 80)
fig.axes[1].set_xlim(1, 80)
fig.axes[0].set_ylim(1, 100000)
fig.axes[1].set_ylim(1, 100000)
#fig.axes[0].set_ylabel("log Power")
#fig.axes[1].set_ylabel("log Power")
#fig.axes[0].set_yscale('log')
#fig.axes[1].set_yscale('log')
#%%
empty_room_raw_filt = empty_room_raw.copy().filter(l_freq=42, h_freq=45)
empty_room_projs = mne.compute_proj_raw(empty_room_raw_filt, n_grad=3, n_mag=3)
mne.viz.plot_projs_topomap(
    empty_room_projs, colorbar=True, vlim="joint", info=empty_room_raw.info
)


# %%
raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif", preload = True).crop(0, 30)
raw.del_proj()

#%%
fig = raw.compute_psd().plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(1, 80)
fig.axes[1].set_xlim(1, 80)
fig.axes[0].set_ylim(1, 10000)
fig.axes[1].set_ylim(1, 10000)
fig.axes[0].set_ylabel("log Power")
fig.axes[1].set_ylabel("log Power")
fig.axes[0].set_yscale('log')
fig.axes[1].set_yscale('log')

#%%
raw.add_proj(empty_room_projs)
raw.apply_proj()

#%%
fig = raw.compute_psd().plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(1, 80)
fig.axes[1].set_xlim(1, 80)
fig.axes[0].set_ylim(1, 10000)
fig.axes[1].set_ylim(1, 10000)
fig.axes[0].set_ylabel("log Power")
fig.axes[1].set_ylabel("log Power")
fig.axes[0].set_yscale('log')
fig.axes[1].set_yscale('log')



# %%
########################
import mne
import os
import matplotlib
matplotlib.use("TkAgg")  # or "Qt5Agg"
import matplotlib.pyplot as plt

raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif")
raw.load_data()

empty_room_raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_erm_raw.fif", preload = True)
empty_room_raw.del_proj()
spectrum = empty_room_raw.compute_psd()
for average in (False, True):
    spectrum.plot(
        average=average,
        dB=False,
        amplitude=True,
        xscale="log",
        picks="data",
        exclude="bads",
    )

empty_room_raw_filt = empty_room_raw.copy().filter(l_freq=56, h_freq=64)
empty_room_projs = mne.compute_proj_raw(empty_room_raw, n_grad=3, n_mag=3)
mne.viz.plot_projs_topomap(
    empty_room_projs, colorbar=True, vlim="joint", info=empty_room_raw.info
)

projs = empty_room_projs[3:]

raw.add_proj(projs, remove_existing=True)
with mne.viz.use_browser_backend("matplotlib"):
    fig = raw.plot(proj=True, order=mags, duration=1, n_channels=2)
fig.subplots_adjust(top=0.9)





#%%
psd_with_proj = empty_room_raw.add_proj(projs).compute_psd(proj=True)
fig = psd_with_proj.plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(1, 80)
fig.axes[1].set_xlim(1, 80)
fig.axes[0].set_ylim(1, 10000)
fig.axes[1].set_ylim(1, 10000)
fig.axes[0].set_ylabel("log Power")
fig.axes[1].set_ylabel("log Power")
fig.axes[0].set_yscale('log')
fig.axes[1].set_yscale('log')

# %%
mags = mne.pick_types(raw.info, meg="mag")
projs = empty_room_projs[3:]

raw.add_proj(projs, remove_existing=True)
with mne.viz.use_browser_backend("matplotlib"):
    fig = raw.plot(proj=True, order=mags, duration=1, n_channels=2)
fig.subplots_adjust(top=0.9)

# %%
raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif")
psd_no_proj = raw.compute_psd(proj=False)
psd_with_proj = raw.add_proj(projs).compute_psd(proj=True)
fig = psd_with_proj.plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(1, 80)
fig.axes[1].set_xlim(1, 80)
fig.axes[0].set_ylim(1, 10000)
fig.axes[1].set_ylim(1, 10000)
fig.axes[0].set_ylabel("log Power")
fig.axes[1].set_ylabel("log Power")
fig.axes[0].set_yscale('log')
fig.axes[1].set_yscale('log')
# %%
#########
raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif", preload = True)
raw_filt = raw.copy().filter(l_freq=42, h_freq=45)
projs = mne.compute_proj_raw(raw_filt, n_grad=3, n_mag=3)

psd_with_proj = raw.add_proj(projs).compute_psd(proj=True)
fig = psd_with_proj.plot(
        average=False,
        dB=False,
        picks="data",
        exclude="bads"
    )
fig.axes[0].set_xlim(1, 80)
fig.axes[1].set_xlim(1, 80)
fig.axes[0].set_ylim(1, 10000)
fig.axes[1].set_ylim(1, 10000)
fig.axes[0].set_ylabel("log Power")
fig.axes[1].set_ylabel("log Power")
fig.axes[0].set_yscale('log')
fig.axes[1].set_yscale('log')

# %%
########################
import mne
import os
import matplotlib
matplotlib.use("TkAgg")  # or "Qt5Agg"
import matplotlib.pyplot as plt

raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest1_raw_tsss.fif", preload = True)
raw_spectrum = raw.compute_psd()

empty_room_raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_erm_raw.fif", preload = True)
empty_room_raw.del_proj()
erm_spectrum = empty_room_raw.compute_psd()

fig = erm_spectrum.plot(
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

fig = raw_spectrum.plot(
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

# %%
raw = mne.io.read_raw_fif("C:/meg/NVAR_preprocessing/MEG/sub_NVAR001/260105/sub_NVAR001_260105_rest2_raw_tsss.fif", preload = True)


filt = raw.copy().filter(l_freq=59, h_freq=61)
projs = mne.compute_proj_raw(filt, n_grad=3, n_mag=3)

#raw.add_proj(projs, remove_existing=True)

raw_spectrum = raw.compute_psd()
fig = raw_spectrum.plot(
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
# %%