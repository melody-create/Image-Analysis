inputDir = getDirectory("Choose folder with .nrrd files");
outputDir = getDirectory("Choose folder for rotated NRRDs");

angle = 180;

list = getFileList(inputDir);
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".nrrd")) {
        // Define full input and output paths
        inputPath = inputDir + list[i];
        outputPath = outputDir + list[i];

        // Open NRRD
        open(inputPath);

        // Rotate 180°
        run("Rotate...", "angle=" + angle + " grid=1 interpolation=Bilinear");

        // Save rotated NRRD
        run("Nrrd ... ", "nrrd=" + outputPath);

        // Close image
        close();

        print("Rotated and saved: " + outputPath);
    }
}

print("All NRRDs rotated 180°");
