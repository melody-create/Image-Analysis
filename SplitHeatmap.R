# Adapted from Complex Heatmap https://jokergoo.github.io/ComplexHeatmap-reference/book/introduction.html

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("ComplexHeatmap")

library(tidyverse) # version 2.0.0
library(RColorBrewer) # version 1.1.3
library(ComplexHeatmap) # version 2.18.0
library(circlize)
library(grid)

setwd("A:/Directory")

tab <- read.csv("activity_green.csv", row.names = 1)
tabmatrix <- as.matrix(tab)

tab_r <- read.csv("activity_red.csv", row.names = 1)
tabmatrix_r <- as.matrix(tab_r)

# Shared color scale ranges
global_min <- 0
global_max <- max(tabmatrix, tabmatrix_r)

# Define consistent color functions
col_fun_r <- colorRamp2(c(global_min, global_max), c("white", "red"))
col_fun_g <- colorRamp2(c(global_min, global_max), c("white", "green"))

# diagonal-split heatmap
ht <- Heatmap(tabmatrix_r,
              name = NULL,
              cluster_rows = FALSE,
              cluster_columns = FALSE,
              rect_gp = gpar(type = "none"),
              show_heatmap_legend = FALSE,  # disable default legend
              border = "black",
              
              cell_fun = function(j, i, x, y, width, height, fill) {
                x0 <- x - width/2; x1 <- x + width/2
                y0 <- y - height/2; y1 <- y + height/2
                
                # upper-left triangle (tabmatrix_r, red)
                grid.polygon(x = c(x0, x1, x0),
                             y = c(y1, y1, y0),
                             gp = gpar(fill = col_fun_r(tabmatrix_r[i, j]), col = NA))
                
                # lower-right triangle (tabmatrix, green)
                grid.polygon(x = c(x1, x1, x0),
                             y = c(y1, y0, y0),
                             gp = gpar(fill = col_fun_g(tabmatrix[i, j]), col = NA))
                
                # outline
                grid.rect(x = x, y = y, width = width, height = height,
                          gp = gpar(col = "white", fill = NA, lwd = 0.5))
              })


# Create shared legends with identical numeric ranges
lgd_r <- Legend(
  title = "Decreased",
  col_fun = col_fun_r,
  at = seq(global_min, global_max, length.out = 3),
  labels = round(seq(global_min, global_max, length.out = 3), 2))

lgd_g <- Legend(
  title = "Increased",
  col_fun = col_fun_g,
  at = seq(global_min, global_max, length.out = 3),
  labels = round(seq(global_min, global_max, length.out = 3), 2))

# Draw final heatmap with both legends
draw(ht, heatmap_legend_list = list(lgd_r, lgd_g))
