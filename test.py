#%%
import mne
import os
import numpy as np

base_dir = "C:/meg/0215_NVAR_sprint_fooof"
stc = mne.read_source_estimate(os.path.join(base_dir, "sub_NVAR008_251113_rest1"))
mean_stc = stc.copy().mean()

# %%

# Keep every other vertex (remove every 2nd)
keep_idx = np.arange(0, mean_stc.data.shape[0]-2, 2)  # 0, 2, 4, 6, ...

# Subset data and vertices
stc_subset = mne.SourceEstimate(
    data=mean_stc.data[keep_idx, :],
    vertices=[mean_stc.vertices[0][keep_idx], mean_stc.vertices[1]],  # adjust depending on whether lh/rh
    tmin=mean_stc.tmin,
    tstep=mean_stc.tstep
)

mean_stc.plot(
    subjects_dir = "C:/meg/NVAR_ICC_day/MRI/freesurfer", 
    subject = "sub_NVAR008", 
    hemi = "both"
)
# %%
