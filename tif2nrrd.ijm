// Convert all TIFFs in a folder to NRRD with same filename
setBatchMode(true);

// Select source folder
source_dir = getDirectory("Choose a folder with .tif images");
list = getFileList(source_dir);

// Output folder
output_dir = source_dir + "NRRD_to_register" + File.separator;
if (!File.exists(output_dir))
    File.makeDirectory(output_dir);

for (i = 0; i < list.length; i++) {

    if (!(endsWith(list[i], ".tif") || endsWith(list[i], ".tiff")))
        continue;

    inputPath = source_dir + list[i];
    open(inputPath);

    // Base filename (no extension)
    baseName = File.getNameWithoutExtension(list[i]);
    print("Processing: " + baseName);

    outputPath = output_dir + baseName + ".nrrd";
    
    // Save as NRRD
    run("Nrrd ... ", "nrrd=" + outputPath);

    close();
    run("Collect Garbage");
}

setBatchMode(false);
print("All done! NRRDs saved to: " + output_dir);
