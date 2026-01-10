// Batch Fiji Macro: process all .czi files in a folder
// Splits channels and saves each as TIF in the same folder

dir = getDirectory("D:/ZF_Images_2025/Chd7 ERK 2025/06272025_ERK/");
list = getFileList(dir);

for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".czi")) {
        inputFile = dir + list[i];
        name = File.getNameWithoutExtension(inputFile);
        print("Processing: " + inputFile);

        // Open with BioFormats (silent)
        run("Bio-Formats Importer", "open=[" + inputFile + "] autoscale color_mode=Default view=Hyperstack stack_order=XYCZT");

        // Split channels
        run("Split Channels");

        // Save each channel as TIF
        n = nImages();
        for (c = 1; c <= n; c++) {
            selectImage(1);
            savePath = dir + name + "_ch" + (c-1) + ".tif";
            print("   Saving channel " + (c-1) + " → " + savePath);
            saveAs("Tiff", savePath);
            close();
        }

        // Close any leftover windows
        while (nImages > 0) {
            selectImage(nImages);
            close();
        }

        print("Finished: " + name);
    }
}

print("Batch processing complete!");
