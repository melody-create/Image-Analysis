#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=64G
#SBATCH --time=72:00:00
#SBATCH --partition=standard

# Load environment
# perl/5.34.0
module load perl
# cmtk 3.3.2
source ~/.bashrc
# Make sure munger is in your PATH
export PATH=$PATH:~/bin

# Paths
MUNGER=~/bin/munger
CMTK_BIN=/cmtk-3.3.2/build/bin/
REF_IMG=Ref/Ref20131120pt14pl2.nrrd
OUT_DIR=/Registered
ROOT_DIR=/imaging_CMTK
cd $ROOT_DIR

echo "Starting CMTK munger registration job on $(date)"

# Loop through each fish NRRD file
for img in images/*.nrrd; do
    [ -f "$img" ] || continue  # skip if no .nrrd files
    name=$(basename "$img" .nrrd)
    echo "Processing: $name"

    $MUNGER \
      -b $CMTK_BIN \
      -T 10 \
      -awr 0102 \
      -X 52 \
      -G 80 \
      -R 3 \
      -A '--accuracy 0.8' \
      -W '--accuracy 1.6' \
      -s $REF_IMG \
      -d $OUT_DIR \
      -v "$img"

    echo "Finished: $name"
    echo "---------------------------------------------------------"
done

echo "CMTK munger job finished on $(date)"
