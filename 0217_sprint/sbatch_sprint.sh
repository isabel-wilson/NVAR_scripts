#!/bin/bash
#SBATCH --time=00:00:10
#SBATCH --mem=0
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=192
#SBATCH --nodes=1
#SBATCH --array=0-7

# Create the logs directory if it does not exist
mkdir -p ./logs/outputs
mkdir -p ./logs/errors

# Activate the virtual environment
module load scipy-stack/2025a
source $HOME/env/bin/activate

# Run the script
inputs=("sub_NVAR008_251016_rest1" "sub_NVAR008_251016_rest1" "sub_NVAR008_251016_rest2" "sub_NVAR008_251016_rest2" "sub_NVAR008_251017_rest1" "sub_NVAR008_251017_rest1" "sub_NVAR008_251017_rest2" "sub_NVAR008_251017_rest2" "sub_NVAR008_251023_rest1" "sub_NVAR008_251023_rest1" "sub_NVAR008_251023_rest2" "sub_NVAR008_251023_rest2" "sub_NVAR008_251113_rest1" "sub_NVAR008_251113_rest1" "sub_NVAR008_251113_rest2" "sub_NVAR008_251113_rest2" "sub_NVAR010_251027_rest1" "sub_NVAR010_251027_rest1" "sub_NVAR010_251027_rest2" "sub_NVAR010_251027_rest2" "sub_NVAR010_251028_rest1" "sub_NVAR010_251028_rest1" "sub_NVAR010_251028_rest2" "sub_NVAR010_251028_rest2" "sub_NVAR010_251103_rest1" "sub_NVAR010_251103_rest1" "sub_NVAR010_251103_rest2" "sub_NVAR010_251103_rest2" "sub_NVAR010_251124_rest1" "sub_NVAR010_251124_rest1" "sub_NVAR010_251124_rest2" "sub_NVAR010_251124_rest2" "sub_NVAR011_251030_rest1" "sub_NVAR011_251030_rest1" "sub_NVAR011_251030_rest2" "sub_NVAR011_251030_rest2" "sub_NVAR011_251031_rest1" "sub_NVAR011_251031_rest1" "sub_NVAR011_251031_rest2" "sub_NVAR011_251031_rest2" "sub_NVAR011_251106_rest1" "sub_NVAR011_251106_rest1" "sub_NVAR011_251106_rest2" "sub_NVAR011_251106_rest2" "sub_NVAR011_251127_rest1" "sub_NVAR011_251127_rest1" "sub_NVAR011_251127_rest2" "sub_NVAR011_251127_rest2")
input=${inputs[$SLURM_ARRAY_TASK_ID]}
python /home/isw3/scratch/sprint/SPRiNT_py.py --input "$input"

# Deactivate the virtual environment
deactivate
