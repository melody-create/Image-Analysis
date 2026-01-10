// Batch Fiji Macro: process all .czi files in a folder
// Splits channels and saves each as TIF in the same folder

dir = getDirectory("D:/ZF_Images/");
list = getFileList(dir);

for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".czi")) {
        inputFile = dir + list[i];
        name = File.getNameWithoutExtension(list[i]);

        // Remove suffix like "_DualSideFusion"
        if (indexOf(name, "_Dual") != -1)
            baseName = substring(name, 0, indexOf(name, "_Dual"));
        else
            baseName = name;
        print("Processing: " + inputFile);

        // Open with Bio-Formats
        run("Bio-Formats Importer",
            "open=[" + inputFile + "] autoscale color_mode=Default view=Hyperstack stack_order=XYCZT");
        // Split channels
        run("Split Channels");
        // Get list of open images
        titles = getList("image.titles");

        ch = 1;
        for (t = 0; t < titles.length; t++) {
            // Only process channel images
            if (startsWith(titles[t], "C")) {
                selectWindow(titles[t]);
                chNum = d2s(ch, 0);
                if (ch < 10) chNum = "0" + chNum;
                savePath = dir + baseName + "_" + chNum + ".tif";
                print(" Saving → " + savePath);
                saveAs("Tiff", savePath);
                close();
                ch++;
            }
        }

        // Close anything still open
        while (nImages() > 0) {
            selectImage(nImages());
            close();
        }
        print("Finished: " + baseName);
    }
}

print("Batch processing complete!");
