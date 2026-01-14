Fiji, bash, matlab, python, and R scripts to perform image analysis on pERK and tERK immuno fluorescent stained zebrafish brain images taken on a Ziess Light Sheet Confocal Microscope (czi files)
Step 1: Preprocessing czi > tif > nrrd using Fiji (ijm)
Step 2: Registration nrrd using computing cluster (bash) then coversion to 8 bit tif with Fiji (ijm)
Step 3: Mapmap creation using matlab
Step 4: Region quantification using python
Step 5: Visualization using R
--- These have been adapted from Ownen Randlett and Summer Thyme's methods and a collaboration between Marsden Lab members Melody Hancock, Dana Hodorovicch-Ruby, and Sureni Sumathipala.
