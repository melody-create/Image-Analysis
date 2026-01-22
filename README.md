Fiji, bash, matlab, python, and R scripts to perform image analysis on pERK and tERK immuno fluorescent stained zebrafish brain images taken on a Ziess Light Sheet Confocal Microscope (czi files)
---Step 1: Preprocessing czi > tif > nrrd > rot 180 nrrd using Fiji (ijm)
---Step 2: Registration of nrrd using CMTK on computing cluster (bash) then coversion to 8 bit smoothed tif with Fiji (ijm)
---Step 3: MAP map creation using matlab
---Step 4: Region quantification using python
---Step 5: Visualization using R
--- These have been adapted from Dr. Owen Randlett (https://github.com/owenrandlett/Z-Brain) and Dr. Summer Thyme (https://github.com/thymelab) methods for use by the Marsden Lab.
