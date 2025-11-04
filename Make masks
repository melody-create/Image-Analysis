import h5py
import dill
import numpy as np

def load_and_flatten_v73_mat(file_path):
    """
    Loads MATLAB v7.3 (.mat) file and flattens nested structs to a Python dict.
    """
    def h5_to_dict(obj):
        data = {}
        for key in obj.keys():
            item = obj[key]
            if isinstance(item, h5py.Group):
                # Recursively flatten groups
                sub_dict = h5_to_dict(item)
                # Merge nested keys
                for sub_key, sub_val in sub_dict.items():
                    data[sub_key] = sub_val
            else:
                arr = np.array(item)
                # Remove singleton dimensions if possible
                if arr.shape == (1,):
                    arr = arr[0]
                data[key] = arr
        return data
    
    with h5py.File(file_path, 'r') as f:
        return h5_to_dict(f)

# Paths to your MATLAB .mat files
mat_files = {
    "mask_noSC": r"A:\mask_noSC.mat",
    "mask": r"A:\mask.mat",
    "all_masks_original": r"A:\all_masks_original.mat"
}

output_dir = r"A:\masks"

for name, mat_path in mat_files.items():
    print(f"Processing {name}...")
    flat_dict = load_and_flatten_v73_mat(mat_path)
    
    dill_path = f"{output_dir}\\{name}.dill"
    # Use highest protocol (5) to safely handle large arrays
    with open(dill_path, "wb") as f:
        dill.dump(flat_dict, f, protocol=5)
    
    print(f"Saved {dill_path}")
