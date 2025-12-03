# Load packages
library(readxl)
library(tidyverse)
library(ggplot2)

setwd("C:/Users/")
getwd()
file <- "Z-score.xlsx"

# Read sheet names: expected WT, HET, MUT
sheet_names <- excel_sheets(file)

# Read each sheet, add a column "Genotype" = sheet name
# Function: read sheet + extract genotype from sheet name
df_list <- lapply(sheet_names, function(s) {
  
  # Extract WT, HET, or MUT from the sheet name
  genotype <- str_extract(s, "WT|HET|MUT")
  
  read_excel(file, sheet = s) %>%
    mutate(Genotype = genotype)
})

# Combine into a single dataframe
df <- bind_rows(df_list)

# Extract Z-Score Slice columns
zscore_cols <- grep("^Z-Score Slice", colnames(df), value = TRUE)
z_matrix <- df[, zscore_cols]

# PCA
pca_res <- prcomp(z_matrix, scale. = TRUE)

# PCA scores + metadata
pca_df <- as.data.frame(pca_res$x)
pca_df$Name <- df$Name
pca_df$Genotype <- df$Genotype

# PCA Plot (color by Genotype)
ggplot(pca_df, aes(x = PC1, y = PC2, color = Genotype, label = Name)) +
  geom_point(size = 1.5) +
  #geom_text(vjust = 0, size = 0) +
  scale_color_manual(values = c(WT = "royalblue", HET = "palegreen3", MUT = "mediumvioletred")) +
  theme_minimal(base_size = 14) +
  labs(
    title = "PCA of First 100 Frames z score",
    x = paste0("PC1 (", round(summary(pca_res)$importance[2,1] * 100, 1), "% variance)"),
    y = paste0("PC2 (", round(summary(pca_res)$importance[2,2] * 100, 1), "% variance)")
  )
