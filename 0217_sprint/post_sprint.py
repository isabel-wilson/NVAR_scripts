# %% [markdown]
# ### Set up

# %%
# Note that code for visualizing sprint psd outputs is in 0205_plot_param.ipynb

# IMPORT PACKAGES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle as pkl
import mne
import copy as copy
from pathlib import Path
from mne.time_frequency import psd_array_welch
import argparse

# GET ARGUMENT
#prefix = "sub_NVAR008_251016_rest1"
parser = argparse.ArgumentParser()
parser.add_argument("--idx", type=str, required=True)
args = parser.parse_args()
prefix = args.idx
print(f"Now working on {prefix}")

# SET PATHS
base_dir = "/home/isw3/scratch/sprint/output"

# CONSTANTS
N_WINDOWS = 115
N_VERTICES = 8196
# Set "example_stc" - this is the original beamformed stc outputted by the generic task-free processing script
# it will be used to get vertex numbers where relevant
example_stc = mne.read_source_estimate(os.path.join(base_dir, "example_stc"))

# %% [markdown]
# ### Postprocess fooof output: Reformat csvs

# %%
# REFORMAT FOOOF CSVS 

def reformat(prefix):
    """
    Input: files prefix_vertex_index.csv (note: vertex index, not vertex number) where each row is window
    Output: files prefix_window_num.csv where each row is vertex index
    """
    for window in range(N_WINDOWS): # Number of windows
        rows = []

        for data_index in range(N_VERTICES): # Number of vertices

            og_csv_path = f"{base_dir}/output/{prefix}_fooof_vertex{data_index}.csv"
            og_df = pd.read_csv(og_csv_path)

            row = og_df.iloc[window].copy()
            row['vertex_index'] = data_index
            rows.append(row)

        pd.DataFrame(rows).to_csv(f"{base_dir}/output/{prefix}_fooof_window{window}.csv", index=False)

reformat(prefix)

