#!/bin/bash

# Configuration
SOURCE_BASE="/home/nanolab/Documents/NVAR/derivatives"
DEST_BASE="/home/nanolab/Documents/NVAR/all_beamformed_stcs"

# Loop over all matching stc folders
for stc_dir in "$SOURCE_BASE"/sub_NVAR*/*/beamformer/stc; do
    [ -d "$stc_dir" ] || continue

    # Extract subject and date from path
    # Path structure: .../sub_NVARxxx/DATE/beamformer/stc
    date=$(basename "$(dirname "$(dirname "$stc_dir")")")
    subject=$(basename "$(dirname "$(dirname "$(dirname "$stc_dir")")")")

    echo "Processing: $subject / $date"

    for rest in rest1 rest2; do
        for hemi in lh rh; do
            
            file=$(find "$stc_dir" -maxdepth 1 -type f -name "*${rest}_raw_tsss_beamformer_stc-${hemi}.stc" | head -n 1)

            new_name="${subject}_${date}_${rest}-${hemi}.stc"
            dest_file="$DEST_BASE/$new_name"

            echo "  Moving: $(basename "$file") -> $new_name"
            cp "$file" "$dest_file"
        done
    done
done
