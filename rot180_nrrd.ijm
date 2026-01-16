inputDir = getDirectory("Choose folder with .nrrd files");
outputDir = getDirectory("Choose folder for rotated NRRDs");

setBatchMode(true);

list = getFileList(inputDir);
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".nrrd")) {

        inputPath = inputDir + list[i];
        outputPath = outputDir + list[i];

        open(inputPath);

        // 180° rotation = flip X + flip Y (no dialogs in batch mode)
        run("Flip Horizontally");
        run("Flip Vertically");

        run("Nrrd ... ", "nrrd=" + outputPath);
        close();

        print("Rotated and saved: " + outputPath);
    }
}

setBatchMode(false);
print("All NRRDs rotated 180°");
