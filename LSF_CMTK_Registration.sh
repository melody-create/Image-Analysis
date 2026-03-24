#!/bin/bash
#BSUB -J cmtk_munger
#BSUB -n 12
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=6.0]"
#BSUB -M 60000
#BSUB -W 46:00
#BSUB -q standard
#BSUB -o cmtk_%J.out
#BSUB -e cmtk_%J.err

set -euo pipefail

# ---- Modules ----
module load perl
module load /usr/local/usrapps/chd7rnaseq/modulefiles/cmtk/3.3.2

# ---- Paths ----
ROOT_DIR=/rsstu/users/k/kcmarsde/CYFIP2_Startle_Project/Sureni_Sumathipala/MAP_mapping/ImagesForKimsPaper
REF_IMG=/rsstu/users/k/kcmarsde/CYFIP2_Startle_Project/Melody_Hancock/map_mapping/Registration/reference/Ref20131120pt14pl2.nrrd
OUT_DIR=$ROOT_DIR/Registered
CMTK_BIN=/usr/local/usrapps/chd7rnaseq/mbhancoc/CMTK-3.3.2/usr/local/lib/cmtk/bin

mkdir -p "$OUT_DIR"
cd "$ROOT_DIR"

echo "=============================================="
echo "Starting CMTK munger job"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "CMTK reformatx: $(which reformatx)"
echo "=============================================="

# ---- Loop over images ----
for img in images/*.nrrd; do
    [ -f "$img" ] || continue
    name=$(basename "$img" .nrrd)
    echo "Processing: $name"

    munger \
      -b $CMTK_BIN \
      -T 10 \
      -awr 0102 \
      -X 52 \
      -G 80 \
      -R 3 \
      -A '--accuracy 0.8' \
      -W '--accuracy 1.6' \
      -s "$REF_IMG" \
      -d "$OUT_DIR" \
      -v "$img"

    echo "Finished: $name"
    echo "----------------------------------------------"
done

echo "CMTK munger job finished on $(date)"
