#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --mem=2048M
#SBATCH --cpus-per-task=4

# Create the logs directory if it does not exist
mkdir -p ./logs/outputs
mkdir -p ./logs/errors

# Activate the virtual environment
source $HOME/env/bin/activate

# Run the script
python /home/isw3/scratch/sprint/SPRiNT_py.py

# Deactivate the virtual environment
deactivate