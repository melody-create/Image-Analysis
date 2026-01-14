// Input warp.nrrd registered images from CMTK and output downsampled and smoothed 8 bit Tiff stacks

max = 65535; // set the max value of the images - 65535 for uint16, or 4096 if uint12 mapped (uint16 for light sheet data since .czi files are acquired at 16-bit)
min = 0; // set the min value for the images

setBatchMode(true);

source_dir = getDirectory("Source Directory");
target_dir = getDirectory("Target Directory");

 list = getFileList(source_dir);

  for (i=0; i<list.length; i++) {
         
        open(source_dir + "/" + list[i]);        
	run("Size...", "width=300 depth=80 constrain average interpolation=Bilinear");
        run("Gaussian Blur...", "sigma=2 stack");
        setMinAndMax(min, max);
	run("8-bit");
	saveAs("tiff", target_dir + "/" + list[i] + "GauSmooth.tiff");
	close();
	showProgress(i, list.length);
	run("Collect Garbage");
  }
