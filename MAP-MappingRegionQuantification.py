#!/usr/bin/env python3
# adapted from https://github.com/thymelab/DownstreamAnalysis/blob/main/sum_intensity_review_allRegion_thres.py

"""
MAP-Mapping Region Quantification Script
----------------------------------------
This script loads 3D MAP-mapping activity images and anatomical region masks,
computes region-wise activation (fraction of active voxels per region) for
each color channel, and outputs CSV tables summarizing results.

Run: python mapmapping_quantify.py
"""

import os
import numpy as np
import pandas as pd
import tifffile
import dill

# ===============================================================
# USER SETTINGS
# ===============================================================

# Input image directory (where your .tif brain stacks are)
file_dir = r"A:\In_Directory"

# Output folder (where CSVs will be saved)
output_dir = r"A:\Out_Directory"

# Path to your mask files
mask_path = r"A:\masks"

# Threshold for "active" pixels
threshold = 10

# Region subset (edit this if you want fewer/more)
selected_keys = ['Diencephalon___Left_Habenula_Vglut2_Cluster', 'Mesencephalon___Torus_Longitudinalis', 'Telencephalon___Olfactory_Bulb', 'Rhombencephalon___Gad1b_Cluster_15', 'Rhombencephalon___Ventrolateral_population_of_serotonergic_neurons', 'Rhombencephalon___Medial_Vestibular_Nucleus', 'Rhombencephalon___Gad1b_Cluster_14', 'Rhombencephalon___Gad1b_Cluster_6', 'Mesencephalon___Otpb_Cluster', 'Rhombencephalon___Rhombomere_5', 'Rhombencephalon___Glyt2_Cluster_8', 'Telencephalon___Anterior_Commisure', 'Rhombencephalon___RoL2', 'Rhombencephalon___Isl1_Stripe_1', 'Diencephalon___Hypothalamus_Vglut2_Cluster_1', 'Rhombencephalon___Neuropil_Region_4', 'Rhombencephalon___Glyt2_Cluster_13', 'Rhombencephalon___RoL3', 'Rhombencephalon___67FDhcrtR_Gal4_Stripe_4', 'Diencephalon___Pineal_Vmat2_cluster', 'Mesencephalon___Vmat2_cluster2', 'Telencephalon___Isl1_cluster_1', 'Diencephalon___Retinal_Arborization_Field_6_AF6', 'Diencephalon___Preoptic_area_Vglut2_cluster', 'Rhombencephalon___Olig2_enriched_areas_in_cerebellum', 'Diencephalon___Dopaminergic_Cluster_3__hypothalamus', 'Rhombencephalon___Inferior_Olive', 'Rhombencephalon___Anterior_Cluster_of_nV_Trigeminal_Motorneurons', 'Rhombencephalon___Glyt2_Cluster_5', 'Rhombencephalon___Glyt2_Stripe_1', 'Telencephalon___Subpallial_Otpb_Cluster_2', 'Diencephalon___Caudal_Hypothalamus', 'Rhombencephalon___Qrfp_neuron_cluster_sparse', 'Rhombencephalon___Gad1b_Cluster_20', 'Ganglia___Lateral_Line_Neuromast_O1', 'Diencephalon___Oxtl_Cluster_4__sparse_in_hypothalamus', 'Diencephalon___Pretectal_dopaminergic_cluster', 'Rhombencephalon___Gad1b_Cluster_8', 'Mesencephalon___Tectum_Neuropil', 'Rhombencephalon___67FDhcrtR__Gal4_Stripe_1', 'Ganglia___Facial_glossopharyngeal_ganglion', 'Telencephalon___Vmat2_cluster', 'Rhombencephalon___Vglut2_Stripe_2', 'Diencephalon___Hypothalamus_Gad1b_Cluster_1', 'Rhombencephalon___Glyt2_Cluster_4', 'Mesencephalon___Isl1_cluster_of_the_mesencephalic_region', 'Rhombencephalon___Interpeduncular_Nucleus', 'Rhombencephalon___RoL__R1', 'Telencephalon___S1181t_Cluster', 'Diencephalon___Dopaminergic_Cluster_2__posterior_tuberculum', 'Diencephalon___Pretectum', 'Rhombencephalon___MiD2', 'Diencephalon___Hypothalamus_Olig2_cluster', 'Ganglia___Lateral_Line_Neuromast_D2', 'Diencephalon___Diffuse_Nucleus_of_the_Intermediate_Hypothalamus', 'Spinal_Cord___Isl1_stripe__motorneurons', 'Rhombencephalon___Glyt2_Cluster_10', 'Diencephalon___Anterior_group_of_the_posterior_tubercular_vmat2_neurons', 'Rhombencephalon', 'Mesencephalon___Vglut2_cluster_1', 'Diencephalon___Retinal_Arborization_Field_1_AF1', 'Rhombencephalon___Rhombomere_6', 'Rhombencephalon___X_Vagus_motorneuron_cluster', 'Rhombencephalon___Tangential_Vestibular_Nucleus', 'Rhombencephalon___Neuropil_Region_2', 'Mesencephalon___Retinal_Arborization_Field_7_AF7', 'Diencephalon___Dopaminergic_Cluster_4_5__posterior_tuberculum_and_hypothalamus', 'Rhombencephalon___Gad1b_Cluster_9', 'Spinal_Cord___Vmat2_Stripe_1', 'Rhombencephalon___Olig2_Stripe', 'Ganglia___Lateral_Line_Neuromast_OC1', 'Rhombencephalon___Gly2_Cluster_6', 'Diencephalon___Pretectal_Gad1b_Cluster', 'Diencephalon___Hypothalamus_Qrfp_neuron_cluster', 'Diencephalon___Preoptic_Area', 'Rhombencephalon___Mauthner', 'Rhombencephalon___MiV2', 'Diencephalon___Otpb_Cluster_2', 'Ganglia___Lateral_Line_Neuromast_D1', 'Diencephalon___Hypothalamus_Hcrt_Neurons', 'Rhombencephalon___Rhombomere_4', 'Diencephalon___Migrated_Area_of_the_Prectectum_M1', 'Rhombencephalon___Otpb_Cluster_3', 'Rhombencephalon___67FDhcrtR__Gal4_Cluster_4', 'Spinal_Cord___Vglut2_Stripe_3', 'Telencephalon___Pallium', 'Diencephalon___Anterior_preoptic_dopaminergic_cluster', 'Rhombencephalon___Gad1b_Cluster_4', 'Rhombencephalon___Glyt2_Stripe_2', 'Rhombencephalon___Vmat2_Cluster_4', 'Diencephalon___Preoptic_area_posterior_dopaminergic_cluster', 'Rhombencephalon___Glyt2_Cluster_9', 'Telencephalon___Postoptic_Commissure', 'Diencephalon___Optic_Chiasm', 'Diencephalon___Oxtl_Cluster_5', 'Rhombencephalon___S1181t_Cluster', 'Rhombencephalon___Eminentia_Granularis', 'Spinal_Cord___Vglut2_Stripe_1', 'Diencephalon___Right_Habenula_Vglu2_Cluster', 'Rhombencephalon___67FDhcrtR__Gal4_Cluster_2_Sparse', 'Rhombencephalon___Rhombomere_3', 'Rhombencephalon___RoM1', 'Rhombencephalon___Ptf1a_Cluster_1', 'Rhombencephalon___Otpb_Cluster_1', 'Rhombencephalon___Spiral_Fiber_Neuron_Anterior_cluster', 'Rhombencephalon___Cerebellum_Gad1b_Enriched_Areas', 'Diencephalon___Olig2_Band_2', 'Rhombencephalon___Isl1_Cluster_3', 'Diencephalon___Isl1_cluster_2', 'Rhombencephalon___Caudal_Ventral_Cluster_Labelled_by_Spinal_Backfills', 'Rhombencephalon___Mauthner_Cell_Axon_Cap', 'Ganglia___Lateral_Line_Neuromast_N', 'Ganglia___Trigeminal_Ganglion', 'Rhombencephalon___Vglut2_Stripe_3', 'Rhombencephalon___MiT', 'Diencephalon___Retinal_Arborization_Field_5_AF5', 'Diencephalon___Retinal_Arborization_Field_2_AF2', 'Telencephalon___Subpallium', 'Rhombencephalon___Rhombomere_7', 'Ganglia___Lateral_Line_Neuromast_SO3', 'Diencephalon___Otpb_Cluster_3', 'Diencephalon___Hypothalamic_VentroLateral_VMAT_cluster', 'Diencephalon___Oxtl_Cluster_1_in_Preoptic_Area', 'Rhombencephalon___Gad1b_Stripe_1', 'Rhombencephalon___Gad1b_Cluster_18', 'Rhombencephalon___Rhombomere_1', 'Diencephalon___Medial_vglut2_cluster', 'Telencephalon___Subpallial_Otpb_strip', 'Rhombencephalon___MiM1', 'Diencephalon___Posterior_Tuberculum', 'Rhombencephalon___Raphe__Superior', 'Mesencephalon___NucMLF_nucleus_of_the_medial_longitudinal_fascicle', 'Mesencephalon___Oxtl_Cluster_Sparse', 'Rhombencephalon___Glyt2_Stripe_3', 'Rhombencephalon___Gad1b_Cluster_3', 'Rhombencephalon___Raphe__Inferior', 'Rhombencephalon___Glyt2_Cluster_1', 'Rhombencephalon___Gad1b_Cluster_19', 'Diencephalon___Hypothalamus_6.7FRhcrtRGal4_cluster_1', 'Mesencephalon___Torus_Semicircularis', 'Rhombencephalon___Lobus_caudalis_cerebelli', 'Rhombencephalon___MiR2', 'Diencephalon___Hypothalamus_Vglut2_Cluster_5', 'Rhombencephalon___Vglut2_cluster_2', 'Rhombencephalon___RoM3', 'Rhombencephalon___MiD3', 'Rhombencephalon___Oculomotor_Nucleus_nIV', 'Rhombencephalon___Valvula_Cerebelli', 'Spinal_Cord___67FDhcrtR__Gal4_Stripe', 'Rhombencephalon___Cerebellum', 'Mesencephalon___Vmat2_cluster_of_paraventricular_organ', 'Rhombencephalon___67FDhcrtR__Gal4_Cluster_5', 'Diencephalon___Oxtl_Cluster_2', 'Spinal_Cord___Neuropil_Region', 'Diencephalon___Hypothalamus_Vglut2_Cluster_2', 'Diencephalon___Preoptic_Otpb_Cluster', 'Rhombencephalon___Gad1b_Cluster_12', 'Rhombencephalon___Vmat2_Cluster_3', 'Rhombencephalon___Small_cluster_of_TH_stained_neurons', 'Rhombencephalon___Vmat2_Cluster_1', 'Diencephalon___Retinal_Arborization_Field_3_AF3', 'Rhombencephalon___Rhombomere_2', 'Telencephalon___Telencephalic_Migrated_Area_4_M4', 'Telencephalon___Vglut2_rind', 'Rhombencephalon___Gad1b_Stripe_3', 'Rhombencephalon___Glyt2_Cluster_11', 'Rhombencephalon___Spiral_Fiber_Neuron_Posterior_cluster', 'Rhombencephalon___Locus_Coreuleus', 'Rhombencephalon___Gad1b_Cluster_10', 'Rhombencephalon___Oxtl_Cluster_2_near_MC_axon_cap', 'Mesencephalon___Oculomotor_Nucleus_nIII', 'Ganglia___Lateral_Line_Neuromast_SO1', 'Diencephalon', 'Diencephalon___Hypothalamus_Olig2_cluster_2', 'Mesencephalon___Ptf1a_Cluster', 'Rhombencephalon___Neuropil_Region_5', 'Ganglia___Eyes', 'Diencephalon___Torus_Lateralis', 'Diencephalon___Retinal_Arborization_Field_4_AF4', 'Rhombencephalon___Glyt2_Cluster_7', 'Diencephalon___Habenula', 'Spinal_Cord___Gad1b_Stripe_1', 'Rhombencephalon___Glyt2_Cluster_12', 'Rhombencephalon___67FDhcrtR_Gal4_Stripe_3', 'Rhombencephalon___VII_Facial_Motor_and_octavolateralis_efferent_neurons', 'Rhombencephalon___Gad1b_Cluster_7', 'Mesencephalon___Sparse_67FRhcrtR_cluster', 'Rhombencephalon___Posterior_Cluster_of_nV_Trigeminal_Motorneurons', 'Diencephalon___Oxtl_Cluster_3', 'Diencephalon___Hypothalamus__Caudal_Hypothalamus_Neural_Cluster', 'Rhombencephalon___Vmat2_Stripe_1', 'Diencephalon___Pineal', 'Telencephalon___Olfactory_bulb_dopaminergic_neuron_areas', 'Diencephalon___Hypothalamus_6.7FRhcrtRGal4_cluster_2', 'Rhombencephalon___Vmat2_Cluster_5', 'Diencephalon___Hypothalamus_s1181t_Cluster', 'Rhombencephalon___Corpus_Cerebelli', 'Mesencephalon___Retinal_Arborization_Field_8_AF8', 'Rhombencephalon___Gad1b_Cluster_11', 'Diencephalon___Otpb_Cluster_1', 'Rhombencephalon___Neuropil_Region_3', 'Diencephalon___Isl1_cluster_3', 'Rhombencephalon___Gad1b_Cluster_17', 'Rhombencephalon___RoV3', 'Ganglia___Lateral_Line_Neuromast_SO2', 'Rhombencephalon___67FDhcrtR__Gal4_Cluster_3', 'Rhombencephalon___Gad1b_Cluster_16', 'Mesencephalon', 'Rhombencephalon___Otpb_Cluster_4', 'Rhombencephalon___Lateral_Reticular_Nucleus', 'Ganglia___Olfactory_Epithelium', 'Diencephalon___Olig2_Band', 'Diencephalon___Otpb_Cluster_4', 'Telencephalon___Subpallial_dopaminergic_cluster', 'Spinal_Cord___Gad1b_Stripe_2', 'Diencephalon___Ventral_Thalamus', 'Spinal_Cord', 'Rhombencephalon___Vmat2_Cluster_2', 'Telencephalon___Subpallial_Gad1b_Cluster', 'Rhombencephalon___Oxtl_Cluster_1_Sparse', 'Rhombencephalon___CaV', 'Rhombencephalon___Area_Postrema', 'Spinal_Cord___Vglut2_Stripe_2', 'Rhombencephalon___Cerebellar__Vglut2_enriched_areas', 'Rhombencephalon___Spinal_Backfill_Vestibular_Population', 'Spinal_Cord___Olig2_Stripe', 'Diencephalon___Dopaminergic_Cluster_7__Caudal_Hypothalamus', 'Telencephalon___Subpallila_Vglut2_Cluster', 'Rhombencephalon___Vmat2_Stripe_3', 'Rhombencephalon___67FDhcrtR__Gal4_Cluster_1', 'Diencephalon___Dorsal_Thalamus', 'Rhombencephalon___Cerebellar_Neuropil_1', 'Spinal_Cord___Glyt2_Stripe', 'Rhombencephalon___67FDhcrtR__Gal4_Stripe_2', 'Rhombencephalon___Gad1b_Stripe_2', 'Ganglia___Posterior_Lateral_Line_Ganglia', 'Rhombencephalon___Gad1b_Cluster_2', 'Spinal_Cord___Vmat2_Stripe_2', 'Diencephalon___Dopaminergic_Cluster_6__hypothalamus', 'Rhombencephalon___Glyt2_Cluster_2', 'Telencephalon___Olig2_Cluster', 'Rhombencephalon___Vglut2_cluster_1', 'Diencephalon___Pituitary', 'Spinal_Cord___Dorsal_Sparse_Isl1_cluster', 'Diencephalon___Isl1_cluster_1', 'Diencephalon___Intermediate_Hypothalamus', 'Diencephalon___Hypothalamus_Vglut2_Cluster_6', 'Rhombencephalon___Gad1b_Cluster_13', 'Ganglia___Vagal_Ganglia', 'Ganglia___Facial_Sensory_Ganglion', 'Mesencephalon___Tectum_Stratum_Periventriculare', 'Rhombencephalon___VII_prime_Facial_Motor_and_octavolateralis_efferent_neurons', 'Rhombencephalon___Neuropil_Region_6', 'Mesencephalon___Retinal_Arborization_Field_9_AF9', 'Rhombencephalon___RoM2', 'Rhombencephalon___Isl1_Cluster_1', 'Diencephalon___Migrated_Posterior_Tubercular_Area_M2', 'Rhombencephalon___CaD', 'Telencephalon___Isl1_cluster_2', 'Rhombencephalon___MiR1', 'Ganglia___Anterior_Lateral_Line_Ganglion', 'Diencephalon___Hypothalamus_Gad1b_Cluster_3_Sparse', 'Rhombencephalon___Vmat2_Stripe_2', 'Telencephalon', 'Diencephalon___Hypothalamus_Vglut2_Cluster_3', 'Rhombencephalon___Glyt2_Cluster_3', 'Rhombencephalon___Olig2_Cluster', 'Telencephalon___Optic_Commissure', 'Rhombencephalon___Glyt2_Cluster_14', 'Diencephalon___Dopaminergic_Cluster_1__ventral_thalamic_and_periventricular_posterior_tubercular_DA_neurons', 'Rhombencephalon___MiV1', 'Rhombencephalon___Vglut2_Stripe_1', 'Rhombencephalon___Vglut2_Stripe_4', 'Ganglia___Statoacoustic_Ganglion', 'Rhombencephalon___Otpb_Cluster_5', 'Rhombencephalon___Gad1b_Cluster_5', 'Diencephalon___Hypothalamus_Gad1b_Cluster_2', 'Mesencephalon___Tegmentum', 'Rhombencephalon___Otpb_Cluster_6', 'Diencephalon___Anterior_pretectum_cluster_of_vmat2_neurons', 'Rhombencephalon___Gad1b_Cluster_1', 'Diencephalon___Rostral_Hypothalamus', 'Diencephalon___Hypothalamus_Vglut2_Cluster_4', 'Diencephalon___Eminentia_Thalami', 'Rhombencephalon___Ptf1a_Stripe', 'Spinal_Cord___Neurons_with_descending_projections_labelled_by_spinal_backfills', 'Rhombencephalon___Isl1_Cluster_2', 'Rhombencephalon___Vglut2_cluster_3', 'Diencephalon___Hypothalamus__Interediate_Hypothalamus_Neural_Cluster', 'Rhombencephalon___Noradrendergic_neurons_of_the_interfascicular_and_Vagal_areas', 'Rhombencephalon___Vglut2_cluster_4', 'Mesencephalon___Medial_Tectal_Band', 'Rhombencephalon___Otpb_Cluster_2__locus_coeruleus', 'Diencephalon___Postoptic_Commissure']

# ===============================================================
# LOAD MASKS
# ===============================================================

print("\nLoading region masks...")
mask_noSC = dill.load(open(os.path.join(mask_path, "whole_brain_mask_no_SpinalCord"), "rb"))
mask = dill.load(open(os.path.join(mask_path, "whole_brain_mask"), "rb"))
all_masks_original = dill.load(open(os.path.join(mask_path, "all_masks_sym_all_good"), "rb"))

# Keep only selected regions
all_masks = {k: v for k, v in all_masks_original.items() if k in selected_keys}

# Compute region sizes (voxel counts)
size_row = pd.Series({k: np.sum(v) for k, v in all_masks.items()})
print(f"Loaded {len(all_masks)} regions.")
print(size_row)

# ===============================================================
# LOAD IMAGE FILES
# ===============================================================

file_names = [f for f in os.listdir(file_dir) if f.endswith(".tif")]
if not file_names:
    raise FileNotFoundError(f"No .tif files found in {file_dir}")

print(f"\nFound {len(file_names)} image files to process.")

# Prepare DataFrames for results
sum_numG = pd.DataFrame(index=[os.path.splitext(f)[0] for f in file_names], columns=selected_keys)
sum_numR = pd.DataFrame(index=[os.path.splitext(f)[0] for f in file_names], columns=selected_keys)

# ===============================================================
# MAIN LOOP
# ===============================================================

for i, file_name in enumerate(file_names, start=1):
    print(f"\n[{i}/{len(file_names)}] Processing {file_name} ...")
    img_path = os.path.join(file_dir, file_name)

    # Load image (expects shape: X, Y, Z, 2)
    brain_im = tifffile.imread(img_path)
    if brain_im.ndim != 4 or brain_im.shape[-1] < 2:
        raise ValueError(f"Unexpected shape {brain_im.shape} in {file_name}")

    # Separate channels
    brain_R = brain_im[..., 0]
    brain_G = brain_im[..., 1]

    # Apply threshold
    brain_R = brain_R * (brain_R >= threshold)
    brain_G = brain_G * (brain_G >= threshold)

    # Compute region-wise activity
    for region, mask_array in all_masks.items():
        active_G = np.sum((brain_G > 0) * mask_array)
        active_R = np.sum((brain_R > 0) * mask_array)
        sum_numG.loc[os.path.splitext(file_name)[0], region] = active_G
        sum_numR.loc[os.path.splitext(file_name)[0], region] = active_R

print("\n Finished processing all files!")

# ===============================================================
# NORMALIZATION & SAVE
# ===============================================================

print("\nNormalizing by region size...")
sum_numG = sum_numG.astype(float).div(size_row, axis=1)
sum_numR = sum_numR.astype(float).div(size_row, axis=1)

# Add size row at the top
sum_numG.loc["RegionSize"] = size_row
sum_numR.loc["RegionSize"] = size_row

# Save results
os.makedirs(output_dir, exist_ok=True)
green_out = os.path.join(output_dir, "region_activity_green.csv")
red_out = os.path.join(output_dir, "region_activity_red.csv")

sum_numG.to_csv(green_out)
sum_numR.to_csv(red_out)

print(f"\n Saved CSVs:")
print(f"  {green_out}")
print(f"  {red_out}\n")
