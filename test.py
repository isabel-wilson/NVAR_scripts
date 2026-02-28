#%%
import mne
import os
base_dir = "C:/meg/0215_NVAR_sprint_fooof"
stc = mne.read_source_estimate(os.path.join(base_dir, "sub_NVAR008_251113_rest1"))
stc.plot(
    subjects_dir = "C:/meg/NVAR_ICC_day/MRI/freesurfer", 
    subject = "sub_NVAR008", 
    initial_time = 0, 
    hemi = "both"
)

# %%
