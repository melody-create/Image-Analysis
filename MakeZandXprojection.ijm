setBatchMode(true); // Run faster without displaying images

// Adapted from Summer Thyme MakeAnXProjection_updated_2024final.ijm
// Summer Thyme github: https://github.com/sthyme/ZFSchizophrenia

// Prompt user for the directory containing input TIFFs
source_dir = getDirectory("Source Directory");
list = getFileList(source_dir);

// Define output folder within the same directory
output_dir = source_dir + "Xprojections" + File.separator;

// Create the output folder if it doesn’t exist
if (!File.exists(output_dir)) {
    File.makeDirectory(output_dir);
}

for (i = 0; i < list.length; i++) {
    SourceImage = source_dir + "BrainOutlineProjections.tif";

    // Skip any non-image files
    if (endsWith(list[i], ".tif") == 0 && endsWith(list[i], ".tiff") == 0) {
        continue;
    }

    ImageName = source_dir + list[i];
    filename = list[i];
    listname = split(filename, ".");
    name = listname[0];

    // Skip the outline image itself
    if (ImageName == SourceImage) {
        continue;
    }

    print("Processing: " + ImageName);

    // Open the source and sample images
    open(SourceImage);
    open(ImageName);
    run("8-bit");
    rename("DeltaMedianStack");

    // Set voxel size metadata
    run("Properties...", "channels=3 slices=80 frames=1 unit=microns pixel_width=1.652 pixel_height=1.652 voxel_depth=3.45");

    // Create Z-projection and reslice projections
    run("Z Project...", "start=1 stop=80 projection=[Sum Slices]");
    selectWindow("DeltaMedianStack");
    run("Reslice [/]...", "output=3.450 start=Left rotate");
    run("Z Project...", "start=1 stop=143 projection=[Sum Slices]");

    // Convert to 8-bit and combine
    selectWindow("SUM_DeltaMedianStack");
    run("8-bit");
    selectWindow("SUM_Reslice of DeltaMedianStack");
    run("8-bit");

    run("Combine...", "stack1=SUM_DeltaMedianStack stack2=[SUM_Reslice of DeltaMedianStack]");
    run("Make Composite", "display=Composite");

    // Merge with white outline and convert to RGB
    run("Split Channels");
    run("Merge Channels...", "c1=[C1-Combined Stacks] c2=[C2-Combined Stacks] c3=[C3-Combined Stacks] c4=BrainOutlineProjections.tif create");
    run("8-bit");
    run("RGB Color", "slices keep");

    // Save output in the 'Xprojections' subfolder
    save_path = output_dir + name + "_RGB_withwhiteoutline.tif";
    saveAs("Tiff", save_path);

    print("Saved to: " + save_path);

    // Clean up memory
    close("*");
    run("Collect Garbage");
}

print("All done!");
